import pickle
import asyncio
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

async def scheduled_save():
    while True:
        await asyncio.sleep(60) 
        db.save_weekly_schedule_to_database(weekly_schedule)
        db.save_tasks_to_database(tasks)
        
async def start_scheduled_save():
    asyncio.create_task(scheduled_save())

# def load_schedule():
#     with open(config.schedule_file, "rb") as fp:
#         return pickle.load(fp)
    
# def load_tasks():
#     with open(config.taks_file, "rb") as fp:
#         return pickle.load(fp)

# def save_weekly_schedule_to_database(weekly_schedule):
#     #print("Сохранение weekly_schedule в базу данных...")
#     with open('data/weekly_schedule.pkl', 'wb') as file:
#         pickle.dump(weekly_schedule, file)

# def save_tasks_to_database(tasks):
#     #print("Сохранение tasks в базу данных...")
#     with open('data/tasks.pkl', 'wb') as file:
#         pickle.dump(tasks, file)