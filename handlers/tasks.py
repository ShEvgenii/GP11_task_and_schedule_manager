from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery 
from datetime import datetime

import logic.utils as utils
import logic.tasks as tsk
import logic.schedule as schdl
from states.states import Gen

from db.data import tasks
import text.text as text
import keyboards.kb as kb

router = Router()

@router.callback_query(F.data == "add_task")
async def add_task(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(Gen.edit_task_time)
    await clbck.message.edit_text(text.edit_task_time)

@router.message(Gen.edit_task_time)
async def edit_task_time(msg: Message, state: FSMContext):
    datetime_str = msg.text.strip()
    if utils.Validator.validate_datetime_format(datetime_str):
        await state.update_data(draft_time=datetime_str)
        await state.set_state(Gen.edit_task_name)
        await msg.answer(text.edit_task_name)
    else:
        await msg.answer(text.edit_correct_task_time)


@router.message(Gen.edit_task_name)
async def edit_task_name(msg: Message, state: FSMContext):
    name = msg.text
    data = await state.get_data()
    time = data.get('draft_time')
    time = datetime.strptime(time, "%d.%m.%y %H:%M")
    task = tsk.Task(name, time)
    tasks[msg.from_user.id].add_task(task)
    await msg.answer(f"Задача \"{name}\" на время {time} успешно создана!")


@router.callback_query(F.data == "delete_task")
async def delete_event(clbck: CallbackQuery, state: FSMContext):
    user_id = clbck.from_user.id
    formatted_tasks = tasks.get(clbck.from_user.id).get_tasks_str()
    await state.set_state(Gen.edit_task_num)
    await clbck.message.delete()
    await clbck.message.answer(f"{formatted_tasks}Введите номер задачи для удаления:")

@router.message(Gen.edit_task_num)
async def delete_event_num(msg: Message, state: FSMContext):
    try:
        tusk_num = int(msg.text)
        user_id = msg.from_user.id
        user_tasks = tasks.get(user_id)
        
        if 1 <= tusk_num <= len(user_tasks.tasks):
            user_tasks.delete_task(tusk_num)
            formatted_tasks = user_tasks.get_tasks_str()
            
            await msg.answer("Задача успешно удалена!")
            await msg.answer(formatted_tasks, reply_markup=kb.exit_kb)
        else:
            await msg.answer("Некорректный номер события. Попробуйте снова.")

    except ValueError:
        await msg.answer("Пожалуйста, введите номер события цифрой.")

@router.callback_query(F.data == "show_tasks")
async def input_text_prompt(clbck: CallbackQuery, state: FSMContext):
    await clbck.message.edit_text(tasks[clbck.from_user.id].get_tasks_str())
