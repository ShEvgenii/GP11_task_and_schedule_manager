from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery 
#import utils
import logic.utils as utils
import logic.tasks as tsk
import logic.schedule as schdl
from states import Gen

from db.data import weekly_schedule, tasks
import text
import keyboards.kb as kb

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    if msg.from_user.id not in weekly_schedule:
        weekly_schedule[msg.from_user.id] = schdl.create_empty_weekly_schedule()
        tasks[msg.from_user.id] = tsk.Tasks()
    await msg.answer(text.greet.format(name=msg.from_user.full_name) + str(msg.from_user.id), reply_markup=kb.menu)

@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
@router.message(F.text == "Назад")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)

@router.callback_query(F.data == "show_schedule")
async def show_schedule(clbck: CallbackQuery, state: FSMContext):
    formatted_schedule = weekly_schedule[clbck.from_user.id].show_weekly_schedule()
    await clbck.message.delete()
    await clbck.message.answer(formatted_schedule, reply_markup=kb.exit_kb)

@router.callback_query(F.data == "edit_schedule")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.edit_schedule)
    await clbck.message.reply("Выбери день", reply_markup=kb.week_kb)

@router.message(Gen.edit_schedule)
async def edit_day_schedule(msg: Message, state: FSMContext):
    day = msg.text
    await state.update_data(draft_day=day)
    
    user_id = msg.from_user.id
    user_schedule = weekly_schedule.get(user_id)
    await state.update_data(weekly_schedule=user_schedule)
    
    await msg.answer(f"Выбран день: {day}\nВыберите действие:", reply_markup=kb.day_schedule_kb)

@router.callback_query(F.data == "add_event")
async def add_task(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.edit_event_time)
    await clbck.message.edit_text(text.edit_event_time)

@router.message(Gen.edit_event_time)
async def edit_event_time(msg: Message, state: FSMContext):
    time = msg.text.strip()
    if utils.validate_time_format(time):
        await state.update_data(draft_time=time)
        await state.set_state(Gen.edit_event_name)
        await msg.answer(text.edit_event_name)
    else:
        await msg.answer(text.edit_event_time)

@router.message(Gen.edit_event_name)
async def edit_event_name(msg: Message, state: FSMContext):
    name = msg.text
    data = await state.get_data()
    time = data.get('draft_time') 
    day = data.get('draft_day')
    
    user_id = msg.from_user.id
    user_schedule = data.get('weekly_schedule')  
    if user_schedule:
        event = schdl.Event(name, time)
        user_schedule.add_event_to_day(day, event)
        
        formatted_schedule = user_schedule.show_weekly_schedule()
        
        await state.update_data(weekly_schedule=user_schedule)
        
        await msg.answer(text.edit_event_name_succes.format(name, time, day))
        await msg.answer(formatted_schedule, reply_markup=kb.exit_kb)
    else:
        await msg.answer(text.edit_event_name_error)

@router.callback_query(F.data == "delete_event")
async def delete_event(clbck: CallbackQuery, state: FSMContext):
    user_id = clbck.from_user.id
    formatted_schedule = weekly_schedule[user_id].show_weekly_schedule()
    await state.set_state(Gen.edit_event_num)
    await clbck.message.delete()
    await clbck.message.answer(f"Номера событий на сегодня:\n{formatted_schedule}\n\nВведите номер события для удаления:")

@router.message(Gen.edit_event_num)
async def delete_event_num(msg: Message, state: FSMContext):
    try:
        event_num = int(msg.text)
        user_id = msg.from_user.id
        user_schedule = weekly_schedule.get(user_id)
        data = await state.get_data()
        day = data.get('draft_day')
        
        if user_schedule:
            if 1 <= event_num <= len(user_schedule.days[day].events):
                del user_schedule.days[day].events[event_num - 1]
                formatted_schedule = user_schedule.show_weekly_schedule()
                
                await msg.answer("Событие успешно удалено!")
                await msg.answer(formatted_schedule, reply_markup=kb.exit_kb)
            else:
                await msg.answer("Некорректный номер события. Попробуйте снова.")
        else:
            await msg.answer("Произошла ошибка. Пожалуйста, начните заново.")
    except ValueError:
        await msg.answer("Пожалуйста, введите номер события цифрой.")


"""
Tasks
"""
@router.callback_query(F.data == "add_task")
async def add_task(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.edit_task_time)
    await clbck.message.edit_text(text.edit_task_time)

@router.message(Gen.edit_task_time)
async def edit_task_time(msg: Message, state: FSMContext):
    datetime_str = msg.text.strip()
    if utils.validate_datetime_format(datetime_str):
        await state.update_data(draft_time=datetime_str)
        await state.set_state(Gen.edit_task_name)
        await msg.answer(text.edit_task_name)
    else:
        await msg.answer("Пожалуйста, введите дату и время в формате ДД.ММ.ГГ ЧЧ:ММ (например, 01.05.22 10:30)")


@router.message(Gen.edit_task_name)
async def edit_task_name(msg: Message, state: FSMContext):
    name = msg.text
    data = await state.get_data()
    time = data.get('draft_time')
    task = tsk.Task(name, time)
    tasks[msg.from_user.id].add_task(task)
    await msg.answer(f"Задача \"{name}\" на время {time} успешно создана!")

@router.callback_query(F.data == "show_tasks")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.edit_text(str(tasks[clbck.from_user.id]))
