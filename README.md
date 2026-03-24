# Agentic Task & Knowledge Chatbot

A modular FastAPI-based **agentic chatbot** that can both answer user queries and take actions using tools.  
The chatbot supports task management, note storage/search, and persistent conversation history.

## Features

- FastAPI backend with automatic Swagger docs
- Agentic chatbot with tool-calling workflow
- Persistent conversation history
- Task creation, listing, filtering, and status updates
- Note creation and keyword search
- SQLite persistence with SQLAlchemy ORM
- `.env`-based configuration
- Modular layered architecture
- Basic automated tests with pytest

## Project Structure

```text
agentic-chatbot/
├── app/
│   ├── api/
│   │   ├── deps.py
│   │   └── routes/
│   │       ├── chat.py
│   │       ├── health.py
│   │       ├── notes.py
│   │       └── tasks.py
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   ├── db/
│   │   ├── base.py
│   │   ├── init_db.py
│   │   ├── models.py
│   │   └── session.py
│   ├── repositories/
│   │   ├── conversation_repository.py
│   │   ├── note_repository.py
│   │   └── task_repository.py
│   ├── schemas/
│   │   ├── chat.py
│   │   ├── note.py
│   │   └── task.py
│   ├── services/
│   │   ├── agent_service.py
│   │   ├── conversation_service.py
│   │   ├── llm_service.py
│   │   ├── note_service.py
│   │   └── task_service.py
│   ├── tools/
│   │   ├── definitions.py
│   │   └── executor.py
│   └── main.py
├── tests/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Requirements
- Python 3.11+
- OpenAI API key or compatible endpoint
## Setup
1. Create virtual environment
```bash
python -m venv .venv
```
2. Activate environment
    - Windows PowerShell
```bash
.venv\Scripts\Activate.ps1
```
    -Windows CMD
```bash
.venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Create .env
    - Copy .env.example to .env and update the values:

5. Run the application
```bash
python run.py
```

# API Documentation

Once the server is running, open:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
## Main Endpoints
- Health
    GET /health
- Chat
    POST /chat
    POST /chat/conversations
    GET /chat/conversations
    GET /chat/conversations/{conversation_id}
- Tasks
    POST /tasks
    GET /tasks
    PATCH /tasks/{task_id}/status
- Notes
    POST /notes
    GET /notes/search?q=keyword

## Example Requests
- Create a task directly
POST /tasks
```json
    {
    "title": "Finish proposal",
    "description": "Submit before Friday"
    }
```
- Chat with the agent
    POST /chat
```json
    {
    "message": "Create a task called finish the README"
    }
```
- Continue a conversation
    POST /chat
```json
    {
    "conversation_id": 1,
    "message": "Now list all my tasks"
    }
```
## Testing
- Run tests with:
```bash
pytest
```
# Design Summary
The project uses a layered architecture:
- routes for HTTP handling
- services for business logic
- repositories for database access
- tools for agent actions
- db for persistence
- core for configuration, logging, and exceptions

