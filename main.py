from openai import OpenAI
from process import get_tasks,add_task,update_task,delete_task
import json

client = OpenAI()



function_map = {
    'get_tasks':get_tasks,
    'add_task':add_task,
    'update_task':update_task,
    'delete_task':delete_task
}


tools  = [
        {
            "type": "function",
            "function": {
                "name": "get_tasks",
                "description": "Retrieve all tasks from the to-do list.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Add a new task to the to-do list.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Title of the task."},
                        "description": {"type": "string", "description": "Description of the task (optional)."}
                    },
                    "required": ["title","description"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update an existing task by its ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "ID of the task to update."},
                        "title": {"type": "string", "description": "New title of the task (optional)."},
                        "description": {"type": "string", "description": "New description of the task (optional)."},
                    },
                    "required": ["task_id","title","description"],
                    "additionalProperties": False
                },
                "strict": True
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task from the to-do list by its ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "ID of the task to delete."}
                    },
                    "required": ["task_id"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
]



def ask_gpt(msg):
    messages = [{"role": "user", "content": msg}]
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
    )
    
    tool_call = completion.choices[0].message.tool_calls
    print(tool_call)
    return tool_call



inp = str(input("enter a query : "))

tool_calls = ask_gpt(inp)

if tool_calls:
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        tool_arguments = json.loads(tool_call.function.arguments)
    
        # Dynamically call the appropriate function
        if tool_name in function_map:
            result = function_map[tool_name](**tool_arguments)  # Call the mapped function with arguments
            print(f"Result: {result} ")
        else:
            print(f"Function '{tool_name}' is not implemented.")