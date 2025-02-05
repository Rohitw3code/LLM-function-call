import streamlit as st
import requests
import pandas as pd
import json
from openai import OpenAI
from process import get_tasks, add_task, update_task, delete_task

client = OpenAI()

# Base URL for the API
BASE_URL = "http://127.0.0.1:5000"

function_map = {
    "get_tasks": get_tasks,
    "add_task": add_task,
    "update_task": update_task,
    "delete_task": delete_task,
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_tasks",
            "description": "Retrieve all tasks from the to-do list.",
            "parameters": {"type": "object", "properties": {}, "required": [], "additionalProperties": False},
            "strict": True,
        },
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
                    "description": {"type": "string", "description": "Description of the task (optional)."},
                },
                "required": ["title", "description"],
                "additionalProperties": False,
            },
            "strict": True,
        },
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
                "required": ["task_id", "title", "description"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task from the to-do list by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer", "description": "ID of the task to delete."},
                },
                "required": ["task_id"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]

# Function to call GPT and get tool responses
def ask_gpt(msg):
    """Send a query to GPT and get tool call responses."""
    messages = [{"role": "user", "content": msg}]

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
    )

    tool_call = completion.choices[0].message.tool_calls
    return tool_call

# Streamlit app
st.title("To-Do List with GPT")
st.subheader("View and Manage Tasks")

# Input query for GPT
query = st.text_input("Enter your query (e.g., add task, update task, view tasks):")

if query:
    # Send the query to GPT and process the tool calls
    tool_calls = ask_gpt(query)

    if tool_calls:
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_arguments = json.loads(tool_call.function.arguments)

            if tool_name in function_map:
                result = function_map[tool_name](**tool_arguments)  # Call the mapped function with arguments
                st.write(f"Result from {tool_name}: {result}")
            else:
                st.error(f"Function '{tool_name}' is not implemented.")

    st.write("Refreshing table...")
    response = requests.get(f"{BASE_URL}/tasks")
    if response.status_code == 200:
        tasks = response.json()
        tasks_df = pd.DataFrame(tasks, columns=["ID", "Title", "Description", "Status"])
        st.table(tasks_df[["ID", "Title", "Description"]])
    else:
        st.error(f"Failed to fetch tasks: {response.status_code}")
