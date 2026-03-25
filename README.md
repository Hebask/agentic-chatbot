# Agentic Task & Knowledge Chatbot

A modular **FastAPI-based agentic chatbot backend** that can both answer user queries and take actions using tools.

Unlike traditional chatbots, this system is designed to:
- understand user intent
- decide when actions are required
- execute backend operations (tasks, notes, etc.)
- persist and manage conversation state

---

## Project Objective

The goal of this project is to build a **fully functional agentic chatbot system** that demonstrates:

- action-taking behavior (not just Q&A)
- clean backend architecture
- modular service design
- proper separation of concerns
- industrial-level coding practices

This project reflects modern AI systems where chatbots act as **intelligent agents** capable of interacting with tools and workflows.

---

## Features

- FastAPI backend with automatic API documentation
- Agentic chatbot with tool-calling workflow
- Persistent conversation history
- Task creation, listing, filtering, and updates
- Note creation and keyword-based search
- SQLite persistence using SQLAlchemy ORM
- Environment-based configuration (`.env`)
- Clean modular architecture (routes → services → repositories)
- Automated testing using pytest

---

## What Makes This Agentic?

Unlike simple chatbots, this system follows an **agent workflow**:

1. Receive user message
2. Analyze intent using the language model
3. Decide if a tool/action is needed
4. Execute the tool (e.g., create task, fetch notes)
5. Return a final response
6. Store conversation history

This allows the chatbot to:
- create tasks
- retrieve information
- manage user data
- behave as a functional assistant

---

## Project Structure

```text
agentic-chatbot/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── tools/
│   └── main.py
├── docs/
│   ├── market_research.md
│   ├── proposal.md
│   └── architecture.md
├── tests/
├── .env.example
├── README.md
├── requirements.txt
└── run.py
```
## Architecture Overview
    The system follows a layered architecture:
        - API Layer → Handles HTTP requests
        - Service Layer → Contains business logic and agent orchestration
        - Repository Layer → Manages database interactions
        - Database Layer → Stores persistent data
        - Tools Layer → Executes actions requested by the agent
    
    This separation improves:
        - maintainability
        - testability
        - scalability

## Requirements
- Python 3.11+
- OpenAI API key (or compatible endpoint)

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
- Windows CMD
```bash
.venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment
- Copy .env.example to .env and update values:
        APP_NAME=Agentic Chatbot
        APP_ENV=development
        APP_DEBUG=true
        APP_HOST=127.0.0.1
        APP_PORT=8000

        DATABASE_URL=sqlite:///./agentic_chatbot.db

        OPENAI_API_KEY=your_api_key_here
        OPENAI_MODEL=gpt-5.4
        OPENAI_BASE_URL=https://api.openai.com/v1

## Running the Application
```bash
python run.py
```

## API Documentation
    - Swagger UI: http://127.0.0.1:8000/docs
    - ReDoc: http://127.0.0.1:8000/redoc

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
- Create a Task
```json
{
  "title": "Finish proposal",
  "description": "Submit before Friday"
}
```
- Chat with Agent
```json
{
  "message": "Create a task called finish the README"
}
```
- Continue Conversation
```json
{
  "conversation_id": 1,
  "message": "Now list all my tasks"
}
```

## Demo Flow
1. Start the server
2. Open Swagger UI
3. Create a conversation
3. Send:
    "Create a task called submit assignment"
4. Then send:
    "List all my tasks"
5. Observe:
    Task is created
    Agent retrieves stored data
    Conversation is persisted

This demonstrates full agentic behavior.

## Testing
- Run:
```bash
pytest
```
## Design Summary
- The project follows a modular layered design:
    Routes → HTTP handling
    Services → business logic
    Repositories → database access
    Tools → agent actions
    DB → persistence
    Core → config, logging, exceptions

## Limitations
    Uses SQLite (not production-scalable)
    No authentication/authorization
    Depends on external LLM API
    No rate limiting or background workers

## Future Improvements
    Add authentication (JWT)
    Switch to PostgreSQL
    Add Docker support
    Implement async task queue
    Add streaming responses
    Improve observability and logging

## Conclusion
This project demonstrates how to build an agentic AI system using FastAPI with clean architecture and real-world backend design principles. It goes beyond traditional chatbots by enabling action-oriented behavior, making it more aligned with modern AI applications.
