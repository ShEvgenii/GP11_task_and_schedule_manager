days= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

class Event:
    def __init__(self, title, time):
        self.title = title
        self.time = time

    def __str__(self) -> str:
        return f"{self.time}: {self.title}"
    
    def get_title(self) -> str:
        return self.title
    
    def get_time(self) -> str:
        return self.time

class DaySchedule:
    def __init__(self, day_of_week):
        self.day_of_week = day_of_week
        self.events = []

    def __sort(self):
        self.events.sort(key=lambda x: x.time)

    def add_event(self, event: Event):
        self.events.append(event)
        self.__sort()

    def show_schedule(self) -> str:
        result = f"{self.day_of_week}:\n"
        for count, event in enumerate(self.events, start=1):
            result += f"{count}. {event}\n"
        result += "\n"
        return result

class WeeklySchedule:
    def __init__(self):
        self.days = {}  

    def add_day_schedule(self, day_of_week: str, day_schedule: DaySchedule):
        self.days[day_of_week] = day_schedule

    def add_event_to_day(self, day_of_week, event):
        if day_of_week in self.days:
            self.days[day_of_week].add_event(event)
        else:
            print(f"No schedule found for {day_of_week}")

    def show_weekly_schedule(self) -> str:
        result = ""
        for day_schedule in self.days.values():
            result += day_schedule.show_schedule()
        return result
    
    def get_day_schedule(self, day:str) -> DaySchedule:
        return self.days[day]

def create_empty_weekly_schedule():
    #days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    empty_weekly_schedule = WeeklySchedule()
    for day in days:
        empty_weekly_schedule.add_day_schedule(day, DaySchedule(day))
    return empty_weekly_schedule

def validate_time_format(time_str):
    try:
        hours, minutes = time_str.split(":")
        if len(hours) != 2 or len(minutes) != 2:
            return False
        if not 0 <= int(hours) <= 23 or not 0 <= int(minutes) <= 59:
            return False
        return True
    except ValueError:
        return False


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

    def print_all_tasks(self) -> str:
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
        
def validate_datetime_format(datetime_str):
    try:
        date_str, time_str = datetime_str.split()
        day, month, year = date_str.split(".")
        hours, minutes = time_str.split(":")
        if len(day) != 2 or len(month) != 2 or len(year) != 2 or len(hours) != 2 or len(minutes) != 2:
            return False
        if not 0 <= int(day) <= 31 or not 0 <= int(month) <= 12 or not 0 <= int(year) <= 99:
            return False
        if not 0 <= int(hours) <= 23 or not 0 <= int(minutes) <= 59:
            return False
        return True
    except ValueError:
        return False
