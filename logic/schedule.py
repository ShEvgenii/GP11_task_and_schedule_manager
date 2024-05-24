days= ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

class Event:
    def __init__(self, title, time):
        self.title = title
        self.time = time

    def __str__(self) -> str:
        return f"{self.time}: {self.title}"

class DaySchedule:
    def __init__(self, day_of_week):
        self.day_of_week = day_of_week
        self.events = []

    def __sort(self):
        self.events.sort(key=lambda x: x.time)

    def add_event(self, event: Event):
        self.events.append(event)
        self.__sort()

    def delete_event(self, index):
        del self.events[index-1]

    def show_schedule(self) -> str:
        result = f"{self.day_of_week}:\n"
        for count, event in enumerate(self.events, start=1):
            result += f"{count}. {event}\n"
        result += "\n"
        return result

class WeeklySchedule:
    def __init__(self):
        self.days = {}
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days_of_week:
            self.days[day] = DaySchedule(day)

    # def create_empty_weekly_schedule(self):
    #     for day in days:
    #         self.add_day_schedule(day, DaySchedule(day))

    # def add_day_schedule(self, day_of_week: str, day_schedule: DaySchedule):
    #     self.days[day_of_week] = day_schedule

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
    

# def create_empty_weekly_schedule():
#     #days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     empty_weekly_schedule = WeeklySchedule()
#     for day in days:
#         empty_weekly_schedule.add_day_schedule(day, DaySchedule(day))
#     return empty_weekly_schedule