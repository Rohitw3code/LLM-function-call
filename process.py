import requests

BASE_URL = "http://127.0.0.1:5000"

def get_tasks():
    """Retrieve all tasks from the API."""
    response = requests.get(f"{BASE_URL}/tasks")
    if response.status_code == 200:
        print("Tasks retrieved successfully:")
        print(response.json())
    else:
        print(f"Failed to retrieve tasks: {response.status_code}")


def add_task(title, description=""):
    """Add a new task using the API."""
    data = {
        "title": title,
        "description": description
    }
    response = requests.post(f"{BASE_URL}/task", json=data)
    if response.status_code == 201:
        print("Task added successfully:")
        print(response.json())
    else:
        print(f"Failed to add task: {response.status_code}")
        print(response.json())


def update_task(task_id, title=None, description=None, status=None):
    """Update an existing task using the API."""
    data = {}
    if title:
        data["title"] = title
    if description:
        data["description"] = description
    if status:
        data["status"] = status

    response = requests.put(f"{BASE_URL}/task/{task_id}", json=data)
    if response.status_code == 200:
        print("Task updated successfully:")
        print(response.json())
    else:
        print(f"Failed to update task: {response.status_code}")
        print(response.json())


def delete_task(task_id):
    """Delete a task using the API."""
    response = requests.delete(f"{BASE_URL}/task/{task_id}")
    if response.status_code == 200:
        print("Task deleted successfully:")
        print(response.json())
    else:
        print(f"Failed to delete task: {response.status_code}")
        print(response.json())

# if __name__ == "__main__":
#     print("Fetching tasks...")
#     get_tasks()

#     print("\nAdding a new task...")
#     add_task("Buy groceries", "Milk, Bread, Eggs")

#     print("\nUpdating a task...")
#     update_task(1, status="completed")

#     print("\nDeleting a task...")
#     delete_task(1)
