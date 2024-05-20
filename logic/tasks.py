class Task:
    def __init__(self, description, time):
        self.description = description
        self.time = time
    
    def __str__(self):
        return f"{self.time}: {self.description}"

class Tasks:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks_str(self) -> str:
        if self.tasks:
            print("Все задачи:")
            for i, task in enumerate(self.tasks, start=1):
                print(f"{i}. {task.description} - {task.time}")
        else:
            print("Нет задач")

    def __str__(self) -> str:
        if self.tasks:
            tasks_str = "\n".join([f"{task.description} - {task.time}" for task in self.tasks])
            return f"Задачи:\n{tasks_str}"
        else:
            return "Нет задач"