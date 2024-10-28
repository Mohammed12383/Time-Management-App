import time
import threading
from datetime import timedelta

class Task:
    def __init__(self, name, duration):
        self.id = int(time.time() * 1000)
        self.name = name
        self.duration = duration
        self.elapsed = 0
        self.total_time_spent = 0
        self.is_running = False

class TimeManagementApp:
    def __init__(self):
        self.tasks = []
        self.timer_thread = None
        self.stop_timer = threading.Event()

    def add_task(self, name, hours, minutes):
        duration = hours * 3600 + minutes * 60
        if duration > 0:
            task = Task(name, duration)
            self.tasks.append(task)
            print(f"Task '{name}' added successfully.")
        else:
            print("Invalid duration. Task not added.")

    def toggle_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.is_running = not task.is_running
                print(f"Task '{task.name}' {'started' if task.is_running else 'paused'}.")
                return
        print("Task not found.")

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        print("Task deleted.")

    def change_duration(self, task_id, hours, minutes):
        for task in self.tasks:
            if task.id == task_id:
                new_duration = hours * 3600 + minutes * 60
                if new_duration > 0:
                    task.duration = new_duration
                    print(f"Duration for task '{task.name}' updated.")
                else:
                    print("Invalid duration. Task not updated.")
                return
        print("Task not found.")

    def format_time(self, seconds):
        return str(timedelta(seconds=seconds))

    def update_tasks(self):
        while not self.stop_timer.is_set():
            for task in self.tasks:
                if task.is_running:
                    task.elapsed = min(task.elapsed + 1, task.duration)
                    task.total_time_spent += 1
            time.sleep(1)

    def start_timer(self):
        self.stop_timer.clear()
        self.timer_thread = threading.Thread(target=self.update_tasks)
        self.timer_thread.start()

    def stop_timer_thread(self):
        self.stop_timer.set()
        if self.timer_thread:
            self.timer_thread.join()

    def display_tasks(self):
        print("\nCurrent Tasks:")
        for task in self.tasks:
            progress = (task.elapsed / task.duration) * 100 if task.duration > 0 else 0
            print(f"ID: {task.id}")
            print(f"Name: {task.name}")
            print(f"Progress: {self.format_time(task.elapsed)} / {self.format_time(task.duration)} ({progress:.2f}%)")
            print(f"Total time spent: {self.format_time(task.total_time_spent)}")
            print(f"Status: {'Running' if task.is_running else 'Paused'}")
            print("-" * 30)

        total_time_spent = sum(task.total_time_spent for task in self.tasks)
        print(f"Overall Total Time Spent: {self.format_time(total_time_spent)}")

    def run(self):
        print("Welcome to the Time Management App!")
        self.start_timer()

        while True:
            print("\nOptions:")
            print("1. Add Task")
            print("2. Toggle Task")
            print("3. Delete Task")
            print("4. Change Task Duration")
            print("5. Display Tasks")
            print("6. Exit")

            choice = input("Enter your choice (1-6): ")

            if choice == '1':
                name = input("Enter task name: ")
                hours = int(input("Enter duration in hours: "))
                minutes = int(input("Enter duration in minutes: "))
                self.add_task(name, hours, minutes)
            elif choice == '2':
                task_id = int(input("Enter task ID to toggle: "))
                self.toggle_task(task_id)
            elif choice == '3':
                task_id = int(input("Enter task ID to delete: "))
                self.delete_task(task_id)
            elif choice == '4':
                task_id = int(input("Enter task ID to change duration: "))
                hours = int(input("Enter new duration in hours: "))
                minutes = int(input("Enter new duration in minutes: "))
                self.change_duration(task_id, hours, minutes)
            elif choice == '5':
                self.display_tasks()
            elif choice == '6':
                print("Exiting the Time Management App. Goodbye!")
                self.stop_timer_thread()
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = TimeManagementApp()
    app.run() 