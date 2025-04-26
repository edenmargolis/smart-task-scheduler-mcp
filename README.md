# Smart Task Scheduler MCP Server

A lightweight and efficient task management server built using the Model Context Protocol (MCP). This server provides smart task scheduling capabilities with priority-based recommendations and easy task management.

## Features

- Add tasks with titles, descriptions, due dates, and priority levels
- View all tasks or filter by status (pending/completed)
- Mark tasks as completed
- Get smart recommendations based on priority and due dates
- Simple and intuitive API interface
- In-memory task storage for fast access

## Prerequisites

- Python 3.8 or higher
- `uv` package manager (for fast Python package installation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/edenmargolis/smart-task-scheduler-mcp.git
cd smart-task-scheduler-mcp
```

2. Install dependencies using `uv`:
```bash
uv pip install fastmcp pydantic python-dateutil
```

3. Install the MCP server:
```bash
uv run mcp install main.py
```

## Usage

### Starting the Server

Run the server using:
```bash
uv run mcp install main.py
```

The server will start and display available tools:
```
Starting Smart Task Scheduler MCP Server...
Available tools:
1. add_task - Add a new task
2. get_tasks - Get all tasks or filter by status
3. complete_task - Mark a task as completed
4. get_task_recommendations - Get smart recommendations

Server is running. You can now use these tools in your Claude desktop app.
```

### API Examples

1. Adding a Task:
```json
{
    "method": "add_task",
    "params": {
        "title": "Quarterly Report Review",
        "description": "Review and analyze Q1 2024 financial reports",
        "due_date": "2024-04-30",
        "priority": "high"
    }
}
```

2. Getting Tasks:
```json
{
    "method": "get_tasks",
    "params": {
        "status": "pending"
    }
}
```

3. Completing a Task:
```json
{
    "method": "complete_task",
    "params": {
        "task_id": "task_1"
    }
}
```

4. Getting Task Recommendations:
```json
{
    "method": "get_task_recommendations",
    "params": {
        "date": "2024-04-25"
    }
}
```

## Project Structure

```
smart-task-scheduler-mcp/
├── main.py              # Main server implementation
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## Dependencies

- `fastmcp`: FastMCP framework for MCP server implementation
- `pydantic`: Data validation and settings management
- `python-dateutil`: Date and time utilities

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastMCP framework for providing the MCP server implementation
- Python community for the excellent libraries used in this project
