tasks = []
def show_tasks():
    if not tasks:
        print("\nNo tasks yet.")
        return

    for i, task in enumerate(tasks, start=1):
        status = "Done!! " if task["completed"] else " "
        print(f"{i}. [{status}] {task['name']}")


def add_task():
    task_name = input("Enter task: ").strip()

    if not task_name:
        print("Task cannot be empty.")
        return

    tasks.append({
        "name": task_name,
        "completed": False
    })

    print("Task added!")


def complete_task():
    show_tasks()

    if not tasks:
        return

    try:
        task_number = int(input("Enter task number to complete: "))

        if task_number < 1 or task_number > len(tasks):
            print("Invalid task number.")
            return

        tasks[task_number - 1]["completed"] = True
        print("Task completed!")

    except ValueError:
        print("Please enter a valid number.")


def delete_task():
    show_tasks()

    if not tasks:
        return

    try:
        task_number = int(input("Enter task number to delete: "))

        if task_number < 1 or task_number > len(tasks):
            print("Invalid task number.")
            return

        deleted_task = tasks.pop(task_number - 1)
        print(f"Deleted: {deleted_task['name']}")

    except ValueError:
        print("Please enter a valid number.")


def main():
    while True:
        print("TODO LIST")
        print("1. Add task")
        print("2. View tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task()

        elif choice == "2":
            show_tasks()

        elif choice == "3":
            complete_task()

        elif choice == "4":
            delete_task()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()