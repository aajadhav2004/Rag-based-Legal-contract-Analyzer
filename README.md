# RAG Based Legal Contract Analyzer

![RAG Based Legal Contract Analyzer](https://raw.githubusercontent.com/aajadhav2004/legal-ai-analyzer/main/project-screenshot.png)

## 🚀 Overview

A production-grade AI-powered legal contract analysis system built with RAG (Retrieval-Augmented Generation) technology. This application helps legal professionals and businesses analyze contracts efficiently with AI-driven insights, risk detection, and intelligent Q&A capabilities.

## ✨ Features

### 🔐 User Authentication

- Secure signup and login system
- MongoDB Atlas integration for user management
- Password hashing with bcrypt
- Session management with Flask-Login

### 📄 Contract Analysis

- **PDF Upload & Processing**: Upload legal contracts in PDF format
- **Automatic Summarization**: Structured contract summary with key details
  - Contract Type
  - Parties Involved
  - Effective Date & Duration
  - Payment Terms
  - Termination Conditions
  - Jurisdiction
  - Key Obligations

### 🔍 Intelligent Features

- **Clause Extraction**: Automatically identifies and extracts important clauses with page numbers
- **Risk Detection**: Identifies potential legal risks with severity levels (Low/Medium/High)
- **Risk Score**: Overall contract risk assessment (1-10 scale) with visual progress bar
- **Source Citations**: Every AI answer includes page numbers and source text for verification

### 💬 RAG-Based Q&A Chatbot

- Ask questions about uploaded contracts
- Strict RAG answering (only from contract content)
- Collapsible source citations with page numbers
- Real-time document status validation

### 🎨 Modern UI/UX

- Beautiful glass morphism design
- Responsive layout for all devices
- Animated risk score visualization
- Full-width navbar with user profile
- Smooth transitions and interactions

## 🛠️ Tech Stack

### Backend

- **Framework**: Flask (Python)
- **AI/ML**:
  - LangChain for RAG pipeline
  - Groq API (Llama 3.1 8B Instant)
  - HuggingFace Embeddings
- **Vector Database**: FAISS
- **Database**: MongoDB Atlas
- **Authentication**: Flask-Login, bcrypt

### Frontend

- HTML5
- CSS3 (Glass Morphism Design)
- Vanilla JavaScript
- Responsive Design

## 📦 Installation

### Prerequisites

- Python 3.8+
- MongoDB Atlas account
- Groq API key

### Setup Steps

1. **Clone the repository**

```bash
git clone https://github.com/aajadhav2004/legal-ai-analyzer.git
cd legal-ai-analyzer
```

2. **Create virtual environment**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
MONGODB_URI=your_mongodb_atlas_uri
SECRET_KEY=your_secret_key_here
```

5. **Run the application**

```bash
python app.py
```

6. **Access the application**

```
http://localhost:5000
```

## 📁 Project Structure

```
legal-ai-analyzer/
├── app.py                 # Main Flask application
├── auth.py               # Authentication logic
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in repo)
├── .gitignore           # Git ignore rules
├── rag/                 # RAG system modules
│   ├── analyzer.py      # Contract analysis logic
│   ├── chunker.py       # Text chunking
│   ├── embeddings.py    # Embedding generation
│   ├── loader.py        # PDF loading
│   ├── qa_system.py     # Q&A system
│   └── vectordb.py      # Vector database operations
├── static/              # Static assets
│   ├── auth.css         # Authentication page styles
│   ├── script.js        # Frontend JavaScript
│   └── style.css        # Main styles
├── templates/           # HTML templates
│   ├── index.html       # Main application page
│   ├── login.html       # Login page
│   └── signup.html      # Signup page
└── uploads/             # Uploaded PDF storage
```

## 🔑 Key Features Explained

### RAG Pipeline

The system uses a sophisticated RAG (Retrieval-Augmented Generation) pipeline:

1. PDF text extraction with page metadata
2. Text chunking for optimal context
3. Vector embeddings generation
4. FAISS vector database creation
5. Semantic search for relevant context
6. LLM-powered answer generation with citations

### Risk Scoring Algorithm

- **High Risk**: 3 points per occurrence
- **Medium Risk**: 2 points per occurrence
- **Low Risk**: 1 point per occurrence
- Final score calculated on 1-10 scale with color-coded visualization

### Security Features

- Password hashing with bcrypt
- Session-based authentication
- Protected routes with login_required decorator
- Secure MongoDB connection

## 🎯 Usage

1. **Sign Up**: Create a new account
2. **Login**: Access your dashboard
3. **Upload Contract**: Select and upload a PDF contract
4. **View Analysis**: Automatically see summary, clauses, risks, and risk score
5. **Ask Questions**: Use the chatbot to query specific contract details
6. **View Sources**: Click "View Sources" to see citations for each answer

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Avinash Jadhav**

- Email: avinashjadhav2468@gmail.com
- GitHub: [@aajadhav2004](https://github.com/aajadhav2004)

## 🙏 Acknowledgments

- LangChain for RAG framework
- Groq for fast LLM inference
- HuggingFace for embeddings
- MongoDB Atlas for database hosting

---

⭐ If you find this project helpful, please give it a star!
