from datetime import datetime

class Task:
    def __init__(self, description, time: datetime):
        self.description = description
        self.time = time
    
    def __str__(self):
        return f"{self.time.strftime("%d.%m.%y %H:%M")} - {self.description}"

class Tasks:
    def __init__(self):
        self.tasks = []

    def __sort(self):
        self.tasks.sort(key=lambda x: x.time)

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.__sort()

    def delete_task(self, index):
        del self.tasks[index-1]

    def get_tasks_str(self) -> str:
        result = f"Все задачи:\n"
        for count, task in enumerate(self.tasks, start=1):
            result += f"{count}. {task}\n"
        result += "\n"
        return result

    # def __str__(self) -> str:
    #     if self.tasks:
    #         tasks_str = "\n".join([f"{task}" for task in self.tasks])
    #         return f"Задачи:\n{tasks_str}"
    #     else:
    #         return "Нет задач"