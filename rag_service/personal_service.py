import os,logging,shutil,chromadb
from django.conf import settings
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document as LangchainDocument
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader


logger = logging.getLogger(__name__)

# Configuration constants
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.3-70b-versatile"
COLLECTION_NAME = "rag_documents"
CHUNK_SIZE = 2500
CHUNK_OVERLAP = 400
RETRIEVER_K = 5
RETRIEVER_FETCH_K = 10


class PersonalRAGService:

    def __init__(self, user_id:int):
        self.user_id = user_id
        self.collection_name = f"user_{self.user_id}_docs"
        self.groq_api_key = settings.GROQ_API_KEY


        self.vector_store_path = os.path.join(
            str(settings.PERSONAL_VECTOR_DB_PATH),
            f"user_{self.user_id}"
        )
        os.makedirs(self.vector_store_path, exist_ok=True)


        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.chroma_client = chromadb.PersistentClient(path=self.vector_store_path)
        self.vector_store=None
        self._load_vector_store()

    def _load_vector_store(self):

        try:
            self.vector_store = Chroma(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
            )
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            self.vector_store = Chroma.from_documents(
                client=self.chroma_client,
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
            )
    

    def process_document(self, file_path: str, doc_id: int) -> int:
        try:

            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return 0
            
            documents = self._load_documents(file_path)
            if not documents:
                logger.error(f"No documents extracted from file: {file_path}")
                return 0
            
            chunks = self._split_documents(documents)

            for chunk in chunks:
                chunk.metadata['doc_id'] = doc_id
            
            if not chunks:
                logger.error(f"No chunks created from documents in file: {file_path}")
                return 0
            
            self._add_to_vector_store(chunks)
            logger.info(f"Processed {len(chunks)} chunks from {file_path}")
            return len(chunks)
        except Exception as e:
            logger.error(f"Error processing document {file_path}: {e}")
            return 0
        
    
    def _load_documents(self, file_path: str) -> list:
        ext = os.path.splitext(file_path)[1].lower()

        loaders = {
            '.pdf': PyPDFLoader,
            '.docx': Docx2txtLoader,
            '.txt': TextLoader,
        }

        loader_class = loaders.get(ext)

        if not loader_class:
            logger.error(f"Unsupported file type: {ext}")
            return []
        return loader_class(file_path).load()
    
    def _split_documents(self, documents: list) -> list:

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
        return splitter.split_documents(documents)
    
    def _add_to_vector_store(self, chunks: list):

        if self.vector_store is None:
            self.vector_store = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                client=self.chroma_client,
                collection_name=self.collection_name
            )
        else:
            self.vector_store.add_documents(chunks)

    def _create_llm(self):
        return ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name=LLM_MODEL,
            temperature=0.2,
        )
    

    def query(self, question: str, chat_history: list = None) -> dict:


        try:
            self._load_vector_store()

            try:
                collection = self.chroma_client.get_collection(name=self.collection_name)
                doc_count = collection.count()

                if doc_count == 0:
                    return {
                        'answer': "No documents available for querying.",
                        'sources': []
                    }
            except Exception as e:
                logger.error(f"Error accessing collection: {e}")
                return {
                    'answer': "No documents available for querying.",
                    'sources': []
                }
            
            retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": RETRIEVER_K
                }
            )

            docs = retriever.invoke(question)

            if not docs:
                return {
                    'answer': "No relevant documents found.",
                    'sources': []
                }
            
            context = "\n\n".join([doc.page_content for doc in docs])

            llm = self._create_llm()

            prompt = PromptTemplate(
                template= """You are a helpful assistant answering questions based on the user's personal documents.

                    Answer ONLY based on the context provided. If the answer is not in the context, say "I couldn't find this information in your documents."

                    Context:
                    {context}

                    Question: {question}

                    Answer:""",
                input_variables=["context", "question"]
            )

            answer = llm.invoke(prompt.format(context=context, question=question)).content


            sources = []
            seen = set()
            for doc in docs:
                source = doc.metadata.get('source', 'Unknown')
                filename = os.path.basename(source)
                if filename not in seen:
                    sources.append({'title': filename, 'type': 'personal_document'})
                    seen.add(filename)

            return {
                'answer': answer,
                'sources': sources
            }
        
        except Exception as e:
            logger.error(f"Error during query: {e}")
            return {
                'answer': "An error occurred while processing your query.",
                'sources': []
            }
        
    def delete_document(self, doc_id:int) -> bool:

        try:
            collection = self.chroma_client.get_collection(name=self.collection_name)

            result= collection.get(where={"doc_id": doc_id})

            if result and result['ids']:
                collection.delete(ids=result['ids'])
                logger.info(f"Deleted document ID {doc_id} from vector store.")
            return True
        except Exception as e:
            logger.error(f"Error deleting document ID {doc_id}: {e}")
            return False
        
    def clear_all(self) -> bool:
        try:
            
            try:
                self.chroma_client.delete_collection(name=self.collection_name)
                logger.info(f"Cleared collection {self.collection_name} from vector store.")
            except Exception as e:
                logger.error(f"Error clearing collection {self.collection_name}: {e}")
            
            if os.path.exists(self.vector_store_path):
                shutil.rmtree(self.vector_store_path)
                logger.info(f"Deleted vector store directory at {self.vector_store_path}.")
            return True
        except Exception as e:
            logger.error(f"Error clearing all data: {e}")
            return False
        
    def get_document_count(self) -> int:
        try:
            collection = self.chroma_client.get_collection(name=self.collection_name)
            return collection.count()
        except Exception as e:
            logger.error(f"Error getting document count: {e}")
            return 0