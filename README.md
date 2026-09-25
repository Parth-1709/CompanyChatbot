# 🤖 Company & Employee Info Assistant

An AI-powered company assistant that combines **SQL database querying** with **PDF-based RAG** to answer questions about employees, company policies, and hiring information.

🔗 **Live Demo:** https://companychatbot-parth.streamlit.app/

## 🚀 Features

* 💬 Conversational AI assistant
* 🗄️ Query employee information using a SQLite database
* 📄 Ask questions about company policies and hiring from a PDF
* 🔍 RAG-based document retrieval using FAISS
* 🧠 Hugging Face embeddings for semantic search
* 🛠️ Agentic tool selection using LangGraph
* 🔄 Conversation persistence using LangGraph checkpointing
* 📉 Automatic conversation summarization for longer conversations
* 📊 Streamlit interface with tool execution callbacks
* 🔐 Groq API key entered securely through the Streamlit sidebar

## 🏗️ Architecture

```text
                        User
                         │
                         ▼
                  Streamlit UI
                         │
                         ▼
                  LangGraph Agent
                    /          \
                   /            \
                  ▼              ▼
          SQL Database Tool   Document Tool
                  │              │
                  ▼              ▼
             SQLite DB        FAISS
                                 │
                                 ▼
                       Hugging Face Embeddings
                                 │
                                 ▼
                           Company PDF
```

The agent decides whether a question requires information from the **employee database** or the **company policy/hiring document**.

## 🛠️ Tech Stack

### AI / LLM

* LangChain
* LangGraph
* Groq
* `openai/gpt-oss-120b`

### RAG

* PyPDF
* FAISS
* Hugging Face Embeddings
* `all-MiniLM-L6-v2`

### Database

* SQLite
* SQLAlchemy
* LangChain SQLDatabase Toolkit

### Application

* Streamlit
* StreamlitCallbackHandler

## 📂 Project Structure

```text
CompanyChatbot/
│
├── employeeApp.py
├── employee.db
├── JD_BTSA_2026.pdf
├── requirements.txt
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd CompanyChatbot
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔑 Groq API Key

The application requires a Groq API key.

Run the application:

```bash
streamlit run employeeApp.py
```

Enter your Groq API key in the sidebar.

The key is provided at runtime and is not hardcoded into the application.

## 💡 Example Questions

### Employee / Database Questions

```text
Show me all employees.
```

```text
Who works in the HR department?
```

```text
What is the salary of the employees in the Engineering department?
```

```text
Show employees ranked by salary.
```

### Company Policy / Hiring Questions

```text
What are the company's hiring policies?
```

```text
What are the eligibility requirements?
```

```text
What does the company policy say about hiring?
```

## 🧠 What I Learned

This project was built to practice integrating multiple concepts into a single agentic application:

* Building agents with LangGraph
* Creating custom tools with LangChain
* Connecting agents to SQL databases
* Implementing RAG with FAISS
* Using embedding models for semantic retrieval
* Managing conversation state with `thread_id`
* Using LangGraph checkpointing
* Integrating LangGraph agents with Streamlit
* Handling errors and application state with Streamlit
* Combining structured data and unstructured documents in one agent

## 🔮 Future Improvements

* Add authentication and user accounts
* Replace SQLite with PostgreSQL
* Add persistent conversation history
* Add source citations for retrieved documents
* Improve document ingestion and chunking
* Add more company documents
* Add support for multiple uploaded PDFs
* Deploy with a production database
* Add a more advanced memory system

## 👨‍💻 Author

**Parth Prakash**

Built as a hands-on project to explore **Agentic AI, RAG, SQL agents, LangGraph, and LLM-powered applications**.
