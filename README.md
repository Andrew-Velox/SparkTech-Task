# RAG Chatbot API

A powerful **Retrieval-Augmented Generation (RAG)** chatbot built with Django REST Framework. This application allows users to upload documents (PDF, DOCX, TXT) and have AI-powered conversations based on their document content using state-of-the-art language models.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Background Task Setup](#background-task-setup)
- [Project Structure](#project-structure)

---

## 🚀 Project Overview

This RAG Chatbot system provides a personal document-based Q&A experience. Each user has their own isolated vector store, ensuring data privacy and personalized responses.

### How It Works

1. **User Registration & Authentication**: Users sign up and receive a welcome email. JWT tokens are used for authentication.
2. **Document Upload**: Users upload documents (PDF, DOCX, TXT) which are processed and chunked.
3. **Vector Embedding**: Document chunks are embedded using Sentence Transformers and stored in ChromaDB.
4. **RAG Query**: When users ask questions, relevant document chunks are retrieved and used as context for the LLM.
5. **AI Response**: The Groq-powered LLM (LLaMA 3.3 70B) generates accurate responses based on the retrieved context.

---

## ✨ Features

- **User Authentication**: JWT-based authentication with signup and login
- **Email Verification**: Welcome emails sent upon registration
- **Document Processing**: Support for PDF, DOCX, and TXT files (up to 10MB)
- **Personal Vector Store**: Each user has isolated document storage
- **RAG-Powered Chat**: AI responses based on user's uploaded documents
- **Chat History**: Persistent conversation history per user
- **Auto Cleanup**: Background task to delete chat history older than 30 days
- **Swagger Documentation**: Interactive API documentation

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Django REST   │────▶│   ChromaDB      │────▶│   Groq LLM      │
│   Framework     │     │   (Vector DB)   │     │   (LLaMA 3.3)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │
        ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│   SQLite DB     │     │   HuggingFace   │
│   (User Data)   │     │   Embeddings    │
└─────────────────┘     └─────────────────┘
```

---

## 🛠️ Technologies Used

### Backend Framework
| Technology | Purpose |
|------------|---------|
| **Django 5.x** | Web framework |
| **Django REST Framework** | API development |
| **drf-spectacular** | OpenAPI/Swagger documentation |

### Authentication & Security
| Technology | Purpose |
|------------|---------|
| **djangorestframework-simplejwt** | JWT authentication |
| **django-cors-headers** | CORS handling |

### AI & Machine Learning
| Technology | Purpose |
|------------|---------|
| **LangChain** | LLM orchestration framework |
| **Groq API** | LLM inference (LLaMA 3.3 70B Versatile) |
| **HuggingFace Transformers** | Embedding generation |
| **Sentence Transformers** | all-MiniLM-L6-v2 embeddings |

### Vector Database
| Technology | Purpose |
|------------|---------|
| **ChromaDB** | Vector storage and similarity search |
| **langchain-chroma** | LangChain integration |

### Document Processing
| Technology | Purpose |
|------------|---------|
| **PyPDF** | PDF file parsing |
| **docx2txt** | DOCX file parsing |

### Background Tasks
| Technology | Purpose |
|------------|---------|
| **django-apscheduler** | Background job scheduling |
| **APScheduler** | Task scheduling engine |

---

## ⚙️ Setup Instructions

### Prerequisites

- Python 3.10+
- pip (Python package manager)
- Groq API Key (get one at [console.groq.com](https://console.groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Andrew-Velox/SparkTech-Task.git
   cd SparkTech-Task
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   ```bash
   # Create .env file in the project root
   touch .env
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Swagger UI: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

---

## 🔐 Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Email Configuration (for sending welcome emails)
EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_email_app_password

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
```

**Note:** For Gmail, you need to generate an App Password:
1. Enable 2-Factor Authentication on your Google account
2. Go to Google Account → Security → 2-Step Verification → App passwords
3. Generate a new app password for "Mail"
4. Use this generated password as `EMAIL_PASSWORD`

### Getting a Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy and paste into your `.env` file

---

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000/
```

### Authentication

All endpoints except `/signup/` and `/login/` require JWT authentication.

Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

---

### 1. User Signup

**Endpoint:** `POST /signup/`

**Description:** Register a new user account. A welcome email will be sent upon successful registration.

**Request Body:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "confirm_password": "SecurePass123"
}
```

**Success Response (201):**
```json
{
    "detail": "Registration successful. Please check your email."
}
```

**Error Response (400):**
```json
{
    "email": ["A user with that email already exists."],
    "confirm_password": ["Passwords don't match."]
}
```

---

### 2. User Login

**Endpoint:** `POST /login/`

**Description:** Authenticate user and retrieve JWT tokens. Accepts either username or email.

**Request Body:**
```json
{
    "username_or_email": "johndoe",
    "password": "SecurePass123"
}
```

**Success Response (200):**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com"
    }
}
```

**Error Response (400):**
```json
{
    "non_field_errors": ["Invalid username/email or password"]
}
```

---

### 3. Upload Document

**Endpoint:** `POST /upload/`

**Description:** Upload a document (PDF, DOCX, TXT) for RAG processing. Maximum file size: 10MB.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Request Body:**
```
file: <binary file>
```

**Success Response (201):**
```json
{
    "id": 1,
    "title": "my_document",
    "file": "/media/user_documents/my_document.pdf",
    "uploaded_at": "2025-12-16T10:30:00Z",
    "processed": true,
    "chunk_count": 25
}
```

**Error Response (400):**
```json
{
    "file": ["Only .pdf, .txt, .docx files are allowed"]
}
```

---

### 4. Chat with Documents

**Endpoint:** `POST /chat/`

**Description:** Send a question and receive an AI-generated response based on your uploaded documents.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "question": "What is the main topic of my document?",
    "chat_history": []
}
```

**Success Response (200):**
```json
{
    "question": "What is the main topic of my document?",
    "answer": "Based on your uploaded documents, the main topic discusses...",
    "sources": [
        {
            "content": "Relevant excerpt from document...",
            "metadata": {
                "doc_id": 1,
                "page": 3
            }
        }
    ]
}
```

**Error Response (500):**
```json
{
    "error": "No documents found. Please upload documents first."
}
```

---

### 5. Get Chat History

**Endpoint:** `GET /chat-history/`

**Description:** Retrieve the logged-in user's chat history (last 50 conversations).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Success Response (200):**
```json
[
    {
        "id": 1,
        "query": "What is the main topic?",
        "response": "The main topic is about...",
        "created_at": "2025-12-16T10:35:00Z"
    },
    {
        "id": 2,
        "query": "Tell me more about section 2",
        "response": "Section 2 covers...",
        "created_at": "2025-12-16T10:36:00Z"
    }
]
```

---

### API Endpoints Summary

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/signup/` | ❌ | Register new user |
| POST | `/login/` | ❌ | Login and get JWT tokens |
| POST | `/upload/` | ✅ | Upload document for RAG |
| POST | `/chat/` | ✅ | Chat with documents |
| GET | `/chat-history/` | ✅ | Get chat history |

---

## ⏰ Background Task Setup

The application includes a background scheduler that automatically cleans up old chat history records.

### Automatic Cleanup Task

- **Task:** Delete chat history older than 30 days
- **Schedule:** Runs daily at midnight (00:00)
- **Implementation:** Uses `django-apscheduler` with `BackgroundScheduler`

### How It Works

1. The scheduler is initialized when the Django application starts
2. A cron job is registered to run at midnight daily
3. The task queries and deletes all `ChatHistory` records older than 30 days

### Configuration

The scheduler is configured in `rag_service/tasks.py`:

```python
from apscheduler.triggers.cron import CronTrigger

# Schedule the cleanup task to run daily at midnight
scheduler.add_job(
    delete_old_chat_history,
    trigger=CronTrigger(hour=0, minute=0),  # Run at midnight
    id="delete_old_chat_history",
    max_instances=1,
    replace_existing=True,
)
```

### Manual Execution

To manually run the cleanup task:

```bash
python manage.py shell
```

```python
from rag_service.tasks import delete_old_chat_history
delete_old_chat_history()
```

### Monitoring

Check the Django admin panel to view scheduled jobs:
- Navigate to: http://127.0.0.1:8000/admin/django_apscheduler/

---

## 📁 Project Structure

```
SparkTech_Task/
├── askrag/                     # Main Django project
│   ├── settings.py            # Project settings
│   ├── urls.py                # Root URL configuration
│   ├── wsgi.py                # WSGI configuration
│   └── asgi.py                # ASGI configuration
│
├── rag_user/                   # User management app
│   ├── models.py              # CustomUser model
│   ├── views.py               # Signup, Login views
│   ├── serializers.py         # User serializers
│   ├── urls.py                # User endpoints
│   ├── tasks.py               # Email sending task
│   └── templates/
│       └── welcome_email.html # Email template
│
├── rag_service/                # RAG service app
│   ├── models.py              # UserDocument, ChatHistory models
│   ├── views.py               # Document, Chat views
│   ├── serializers.py         # Document, Chat serializers
│   ├── urls.py                # Service endpoints
│   ├── personal_service.py    # RAG processing logic
│   ├── tasks.py               # Background cleanup task
│   └── signals.py             # Django signals
│
├── media/
│   └── user_documents/        # Uploaded documents
│
├── vector_db/
│   └── personal/              # User-specific vector stores
│       └── user_<id>/         # ChromaDB data per user
│
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── README.md                  # This file
```

---

## 💡 Technical Implementation Details

### How was the RAG pipeline integrated for the chatbot?

The RAG pipeline works by first processing uploaded documents into smaller chunks using LangChain's text splitters. Each chunk gets converted into vector embeddings using the `all-MiniLM-L6-v2` model from Sentence Transformers. These embeddings are stored in ChromaDB, which acts as our vector database.

When a user asks a question, the system converts that question into an embedding and searches ChromaDB for the most relevant document chunks (using similarity search). These retrieved chunks provide context to the LLM, allowing it to generate accurate, document-specific answers rather than just general responses. This approach significantly reduces hallucinations and ensures the chatbot stays grounded in the user's actual documents.

Having worked on a similar RAG-based project before, I was already familiar with the document processing workflow and vector similarity search concepts, which made the implementation smoother. However, this project had its own challenges, particularly around isolating each user's vector store and optimizing the chunk sizes for different document types.

### Why this database and model structure?

I chose SQLite for storing user data and chat history because it's lightweight, requires no additional setup, and works perfectly for development and small to medium deployments. The model structure follows Django best practices with two main apps:

- `rag_user` handles authentication and user management
- `rag_service` manages documents and chat functionality

Each user gets their own isolated ChromaDB collection (`user_{id}_docs`), which ensures complete data privacy between users. The `ChatHistory` model stores conversations with timestamps, making it easy to retrieve recent chats and clean up old ones. The `UserDocument` model tracks uploaded files and their processing status, including chunk counts for monitoring.

### How was JWT authentication implemented?

JWT authentication uses `djangorestframework-simplejwt` with a custom login system that accepts either username or email. Here's how security is handled:

- Passwords are hashed using Django's PBKDF2 algorithm before storage
- JWT tokens are issued on successful login with both access and refresh tokens
- Access tokens expire after a short period for security
- All sensitive endpoints require valid JWT tokens in the Authorization header
- User passwords are marked as `write_only` in serializers to prevent exposure in responses
- Email addresses are converted to lowercase to prevent duplicate accounts

The signup process includes password confirmation validation and checks for existing users before account creation.

### How does response generation work with the AI model?

After retrieving relevant document chunks from ChromaDB, the system builds a prompt that includes both the user's question and the retrieved context. This prompt gets sent to Groq's API, which runs the LLaMA 3.3 70B model.

The model uses the retrieved documents as factual grounding to generate its response. I configured the retriever to fetch the top 5 most relevant chunks, which balances between providing enough context and not overwhelming the model's context window. The sources are also returned to the user, so they can see which parts of their documents were used to generate the answer.

LangChain's prompt templates ensure consistent formatting, and the RAG pattern means the model can answer questions about content it wasn't originally trained on.

### How are background tasks scheduled?

Background tasks use `django-apscheduler` with a cron trigger set to run at midnight daily. The scheduler initializes when Django starts up through the app's `ready()` method.

The cleanup task queries the database for `ChatHistory` records older than 30 days and deletes them in bulk. I chose 30 days as a reasonable retention period that balances storage costs with user convenience. The task logs its activity so we can monitor how much data is being cleaned up.

The scheduler uses Django's database as a job store, which means scheduled jobs persist even if the server restarts. I set `max_instances=1` to prevent multiple instances of the cleanup task from running simultaneously.

### What testing strategies were used?

Testing focused on several key areas:

1. **Authentication**: Tested signup validation (duplicate emails, password matching), login with both username and email, and JWT token generation
2. **Document Upload**: Verified file type validation, size limits, and the processing pipeline from upload to embedding storage
3. **RAG Functionality**: Tested document chunking, embedding generation, similarity search, and response generation with various question types
4. **Background Tasks**: Manually triggered the cleanup task to verify it correctly identifies and deletes old records

I also used Swagger UI extensively for integration testing, which made it easy to test the full request/response cycle for each endpoint.

### What external services were integrated?

Three main external services power this application:

1. **Groq API**: Provides access to the LLaMA 3.3 70B model for response generation. I chose Groq because it offers fast inference and generous free tier limits. Configuration just requires setting the API key in the environment.

2. **HuggingFace**: Supplies the embedding model (`all-MiniLM-L6-v2`) which runs locally. This model was chosen for its good balance of speed and accuracy for semantic search tasks.

3. **Gmail SMTP**: Handles sending welcome emails to new users. This requires generating an app password from Google's account settings and configuring the SMTP credentials.

All three services are configured through environment variables, making it easy to swap providers or update credentials without touching the code.

### How could this be expanded?

Here are some ideas for future enhancements:

**Real-time knowledge base updates**: Implement webhooks or file watchers to automatically reprocess documents when they're updated. Could also add incremental updates to the vector store rather than full reprocessing.

**Multi-user chat sessions**: Add a `ChatRoom` model with many-to-many relationships to users. WebSocket support through Django Channels would enable real-time messaging. Each room could have its own shared document collection.

**Better document management**: Add folders/tags for organization, support for more file types (Excel, PowerPoint), and OCR for scanned PDFs.

**Advanced RAG features**: Implement hybrid search (combining vector similarity with keyword matching), query rewriting for better retrieval, and citation tracking to show exactly which document sentences were used.

**Scalability improvements**: Move to PostgreSQL with pgvector for larger deployments, add Redis for caching frequent queries, and use Celery for more robust background task processing.

**Analytics**: Track which documents users query most, monitor response quality, and add user feedback mechanisms to improve the system over time.

---

## 📝 License

This project is created for SparkTech evaluation purposes.

---

## 📧 Support

For questions or issues, please open an issue in the repository.
