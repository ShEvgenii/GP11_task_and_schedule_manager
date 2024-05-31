import pickle
import config

import logic.tasks as tsk
import logic.schedule as schdl

class DataBase():
    def __init__(self, schedule_file, taks_file):
        self.schedule_file = schedule_file
        self.taks_file = taks_file

    def load_schedule(self) -> schdl.WeeklySchedule:
        with open(self.schedule_file, "rb") as fp:
            return pickle.load(fp)

    def load_tasks(self) -> tsk.Tasks:
        with open(self.taks_file, "rb") as fp:
            return pickle.load(fp) 

    def save_weekly_schedule_to_database(self, weekly_schedule: schdl.WeeklySchedule):
        with open(self.schedule_file, 'wb') as file:
            pickle.dump(weekly_schedule, file)

    def save_tasks_to_database(self, tasks: tsk.Tasks):
        with open(self.taks_file, 'wb') as file:
            pickle.dump(tasks, file)


db = DataBase(config.schedule_file, config.taks_file)

weekly_schedule = db.load_schedule()
tasks = db.load_tasks()
