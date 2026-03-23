TOOLS = [
    {
        "type": "function",
        "name": "create_task",
        "description": "Create a new task with a required title and an optional description.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Short task title."
                },
                "description": {
                    "type": "string",
                    "description": "Optional task description."
                }
            },
            "required": ["title"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "list_tasks",
        "description": "List all current tasks.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "update_task_status",
        "description": "Update a task status using its numeric task ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "The numeric ID of the task."
                },
                "status": {
                    "type": "string",
                    "description": "New status value, for example pending, in_progress, or completed."
                }
            },
            "required": ["task_id", "status"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "save_note",
        "description": "Save a note with optional tags and importance flag.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The note text to store."
                },
                "tags": {
                    "type": "string",
                    "description": "Optional comma-separated tags."
                },
                "is_important": {
                    "type": "boolean",
                    "description": "Whether this note is important."
                }
            },
            "required": ["content"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "search_notes",
        "description": "Search saved notes by keyword.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keyword or phrase to search for in notes."
                }
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
]