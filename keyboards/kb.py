from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

menu = [[InlineKeyboardButton(text="Редактировать расписание", callback_data="edit_schedule")],
            [InlineKeyboardButton(text="Показать расписание", callback_data="show_schedule")],
            [InlineKeyboardButton(text="Создать задачу", callback_data="add_task")],
            [InlineKeyboardButton(text="Удалить задачу", callback_data="delete_task")],
            [InlineKeyboardButton(text="Показать задачи", callback_data="show_tasks")]]

menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])

week_kb = [[KeyboardButton(text="Monday"), KeyboardButton(text="Tuesday")],
            [KeyboardButton(text="Wednesday"), KeyboardButton(text="Thursday")],
            [KeyboardButton(text="Friday"), KeyboardButton(text="Saturday")],
            [KeyboardButton(text="Sunday"), KeyboardButton(text="Назад")]]

week_kb = ReplyKeyboardMarkup(keyboard=week_kb, resize_keyboard=True, one_time_keyboard=True)

day_schedule_kb = [[InlineKeyboardButton(text="Добавить событие", callback_data="add_event")],
                    [InlineKeyboardButton(text="Удалить событие", callback_data="delete_event")]]

day_schedule_kb = InlineKeyboardMarkup(inline_keyboard=day_schedule_kb)



