from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):
    edit_task_time = State()
    edit_task_name = State()
    edit_schedule = State()
    edit_event_time = State()
    edit_event_name = State()
    edit_event_num = State()