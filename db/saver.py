import asyncio
from db.data import db, weekly_schedule, tasks

class Saver:
    async def scheduled_save(self):
        while True:
            await asyncio.sleep(60) 
            db.save_weekly_schedule_to_database(weekly_schedule)
            db.save_tasks_to_database(tasks)
            
    async def start_scheduled_save(self):
        asyncio.create_task(self.scheduled_save())