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
   git clone <repository-url>
   cd SparkTech_Task
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

5. **Configure environment variables** (see [Environment Variables](#environment-variables))

6. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Swagger UI: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

---

## 🔐 Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Email Configuration (for sending welcome emails)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Django Settings (optional)
SECRET_KEY=your_secret_key_here
DEBUG=True
```

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

## 📝 License

This project is created for SparkTech evaluation purposes.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Support

For questions or issues, please open an issue in the repository.
