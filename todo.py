import json
import os
from datetime import datetime

class Task:
    def __init__(self, title, description=""):
        self.title = title
        self.description = description
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.completed = False

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "completed": self.completed
        }


class ToDoList:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.tasks = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.tasks = []

    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, title, description=""):
        task = Task(title, description)
        self.tasks.append(task.to_dict())
        self.save_tasks()
        print(f"✅ Task '{title}' added successfully!")

    def view_tasks(self):
        if not self.tasks:
            print("📂 No tasks found.")
            return
        print("\n--- To-Do List ---")
        for idx, task in enumerate(self.tasks, start=1):
            status = "✔ Done" if task["completed"] else "❌ Pending"
            print(f"{idx}. {task['title']} ({status}) | {task['description']} | Added: {task['created_at']}")

    def mark_complete(self, task_number):
        try:
            self.tasks[task_number - 1]["completed"] = True
            self.save_tasks()
            print(f"🎉 Task {task_number} marked as completed!")
        except IndexError:
            print("⚠️ Invalid task number.")

    def delete_task(self, task_number):
        try:
            removed = self.tasks.pop(task_number - 1)
            self.save_tasks()
            print(f"🗑️ Task '{removed['title']}' deleted successfully!")
        except IndexError:
            print("⚠️ Invalid task number.")


def main():
    todo = ToDoList()

    while True:
        print("\n==== To-Do List Manager ====")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Mark Task as Completed")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter description (optional): ")
            todo.add_task(title, description)
        elif choice == "2":
            todo.view_tasks()
        elif choice == "3":
            todo.view_tasks()
            try:
                num = int(input("Enter task number to mark complete: "))
                todo.mark_complete(num)
            except ValueError:
                print("⚠️ Please enter a valid number.")
        elif choice == "4":
            todo.view_tasks()
            try:
                num = int(input("Enter task number to delete: "))
                todo.delete_task(num)
            except ValueError:
                print("⚠️ Please enter a valid number.")
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
