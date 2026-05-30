import json
import os
from datetime import datetime

FILE_NAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Warning: Could not read tasks file. Starting fresh.")
        return []

def save_tasks(tasks):
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(tasks, file, indent=4)
    except OSError as e:
        print(f"Error saving tasks: {e}")


def display_tasks(tasks):
    print("\n===== YOUR TASKS =====")
    if len(tasks) == 0:
        print("No tasks available.\n")
        return

    for i in range(len(tasks)):
        task = tasks[i]
        status = "✔ Done" if task["done"] else "❌ Pending"

        extras = ""
        if task.get("due_date"):
            extras += f"  Due: {task['due_date']}"
        if task.get("tags"):
            extras += f"  Tags: {', '.join(task['tags'])}"

        print(f"{i + 1}. {task['title']} [{status}]{extras}")
    print()


def add_task(tasks):
    title = input("Enter task title: ").strip()
    if title == "":
        print("Task title cannot be empty!")
        return

    due_date = input("Enter due date (YYYY-MM-DD) or press Enter to skip: ").strip()
    if due_date != "":
        try:
            datetime.strptime(due_date, "%Y-%m-%d")  # validate format
        except ValueError:
            print("Invalid date format. Due date will not be saved.")
            due_date = ""

    tags_input = input("Enter tags separated by commas or press Enter to skip: ").strip()
    tags = []
    if tags_input != "":
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip() != ""]

    tasks.append({
        "title":    title,
        "done":     False,
        "due_date": due_date if due_date != "" else None,
        "tags":     tags
    })
    print("Task added successfully!")


def delete_task(tasks):
    display_tasks(tasks)
    if len(tasks) == 0:
        return
    try:
        index = int(input("Enter task number to delete: ")) - 1
        if index < 0 or index >= len(tasks):
            print("Invalid task number!")
            return
        removed = tasks.pop(index)
        print(f"Deleted: {removed['title']}")
    except ValueError:
        print("Please enter a valid number!")


def mark_task_done(tasks):
    display_tasks(tasks)
    if len(tasks) == 0:
        return
    try:
        index = int(input("Enter task number to mark as done: ")) - 1
        if index < 0 or index >= len(tasks):
            print("Invalid task number!")
            return
        if tasks[index]["done"]:
            print(f"Task is already done: {tasks[index]['title']}")
            return
        tasks[index]["done"] = True
        print(f"Marked as done: {tasks[index]['title']}")
    except ValueError:
        print("Please enter a valid number!")


def filter_by_tag(tasks):
    tag = input("Enter tag to filter by: ").strip().lower()
    if tag == "":
        print("Tag cannot be empty!")
        return

    matches = []
    for task in tasks:
        task_tags = [t.lower() for t in task.get("tags", [])]
        if tag in task_tags:
            matches.append(task)

    print(f"\n===== TASKS TAGGED '{tag}' =====")
    if len(matches) == 0:
        print("No tasks found with that tag.\n")
        return

    for i in range(len(matches)):
        status = "✔ Done" if matches[i]["done"] else "❌ Pending"
        print(f"{i + 1}. {matches[i]['title']} [{status}]")
    print()


def show_menu():
    print("\n====== TO-DO MENU ======")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Delete Task")
    print("4. Mark Task as Done")
    print("5. Filter by Tag")
    print("6. Exit")


def main():
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            display_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            mark_task_done(tasks)
        elif choice == "5":
            filter_by_tag(tasks)
        elif choice == "6":
            save_tasks(tasks)
            print("Exiting... Tasks saved successfully!")
            break
        else:
            print("Invalid choice. Please try again.")

        save_tasks(tasks)  


if __name__ == "__main__":
    main()
