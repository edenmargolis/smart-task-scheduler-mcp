# server.py
from mcp.server.fastmcp import FastMCP
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

# Create an MCP server for Smart Task Scheduler
mcp = FastMCP(
    name="Smart Task Scheduler",
    description="A smart task scheduler that helps you manage and optimize your daily tasks.",
    version="1.0.0",
    author="Eden Margolis",
    tools=[
        {
            "name": "add_task",
            "description": "Add a new task to your schedule",
            "parameters": {
                "title": {
                    "type": "string",
                    "description": "Title of the task"
                },
                "description": {
                    "type": "string",
                    "description": "Description of the task"
                },
                "due_date": {
                    "type": "string",
                    "description": "Due date in ISO format (YYYY-MM-DD)"
                },
                "priority": {
                    "type": "string",
                    "description": "Priority level (high, medium, low)",
                    "enum": ["high", "medium", "low"]
                }
            }
        },
        {
            "name": "get_tasks",
            "description": "Get all tasks or filter by status",
            "parameters": {
                "status": {
                    "type": "string",
                    "description": "Filter tasks by status (all, pending, completed)",
                    "enum": ["all", "pending", "completed"],
                    "default": "all"
                }
            }
        },
        {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "task_id": {
                    "type": "string",
                    "description": "ID of the task to complete"
                }
            }
        },
        {
            "name": "get_task_recommendations",
            "description": "Get smart recommendations for task scheduling",
            "parameters": {
                "date": {
                    "type": "string",
                    "description": "Date to get recommendations for (YYYY-MM-DD)",
                    "default": "today"
                }
            }
        }
    ]
)

class Task(BaseModel):
    """Model for task data"""
    id: str
    title: str
    description: str
    due_date: str
    priority: str
    status: str = "pending"
    created_at: str
    completed_at: Optional[str] = None

# In-memory storage for tasks
tasks: Dict[str, Task] = {}

@mcp.tool()
def add_task(title: str, description: str, due_date: str, priority: str) -> Dict[str, Any]:
    """
    Add a new task to the scheduler.
    
    Args:
        title: Title of the task
        description: Description of the task
        due_date: Due date in ISO format
        priority: Priority level (high, medium, low)
        
    Returns:
        Dictionary containing the created task
    """
    task_id = f"task_{len(tasks) + 1}"
    task = Task(
        id=task_id,
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        created_at=datetime.now().isoformat()
    )
    tasks[task_id] = task
    return task.dict()

@mcp.tool()
def get_tasks(status: str = "all") -> List[Dict[str, Any]]:
    """
    Get all tasks or filter by status.
    
    Args:
        status: Filter tasks by status (all, pending, completed)
        
    Returns:
        List of tasks matching the filter
    """
    if status == "all":
        return [task.dict() for task in tasks.values()]
    return [task.dict() for task in tasks.values() if task.status == status]

@mcp.tool()
def complete_task(task_id: str) -> Dict[str, Any]:
    """
    Mark a task as completed.
    
    Args:
        task_id: ID of the task to complete
        
    Returns:
        Updated task data
    """
    if task_id not in tasks:
        return {"error": "Task not found"}
    
    task = tasks[task_id]
    task.status = "completed"
    task.completed_at = datetime.now().isoformat()
    return task.dict()

@mcp.tool()
def get_task_recommendations(date: str = "today") -> Dict[str, Any]:
    """
    Get smart recommendations for task scheduling.
    
    Args:
        date: Date to get recommendations for
        
    Returns:
        Dictionary containing task recommendations
    """
    if date == "today":
        date = datetime.now().date().isoformat()
    
    # Get pending tasks
    pending_tasks = [task for task in tasks.values() if task.status == "pending"]
    
    # Sort tasks by priority and due date
    sorted_tasks = sorted(
        pending_tasks,
        key=lambda x: (
            {"high": 0, "medium": 1, "low": 2}[x.priority],
            x.due_date
        )
    )
    
    # Generate recommendations
    recommendations = {
        "date": date,
        "recommended_tasks": [
            {
                "task_id": task.id,
                "title": task.title,
                "priority": task.priority,
                "due_date": task.due_date,
                "reason": f"High priority task due on {task.due_date}" if task.priority == "high"
                else f"Medium priority task due on {task.due_date}" if task.priority == "medium"
                else f"Low priority task due on {task.due_date}"
            }
            for task in sorted_tasks[:5]  # Recommend top 5 tasks
        ]
    }
    
    return recommendations

if __name__ == "__main__":
    print("Starting Smart Task Scheduler MCP Server...")
    print("Available tools:")
    print("1. add_task - Add a new task")
    print("2. get_tasks - Get all tasks or filter by status")
    print("3. complete_task - Mark a task as completed")
    print("4. get_task_recommendations - Get smart recommendations")
    print("\nServer is running. You can now use these tools in your Claude desktop app.")
    mcp.run()