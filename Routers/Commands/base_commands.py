from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from Routers.Commands.reg_handler import reg_button, check_button, get_sheet_and_row_by_user_id, delete_row_and_shift_up
from keyboards.start_keyboard import ButtonText, get_on_start_kb

import gspread
import time

router = Router(name=__name__)


@router.message(CommandStart())
async def process_start(message: Message):
    await message.answer(
        text=f"""Здравствуйте, {message.from_user.full_name}!
Выберите подходящий пункт в меню""",
        reply_markup=get_on_start_kb()
    )


@router.message(Command("help"))
async def process_help(message: Message):
    text = "Данный бот предназначен для регистрации участников квизов"
    await message.answer(text=text)


@router.message(F.text == ButtonText.REG)
async def handle_reg_button(message: Message):
    try:
        await message.answer(text="Проверяю доступные даты...")
        user_id = message.from_user.id
        if reg_button(user_id) != False:
            await message.answer(
                text="Выберите подохдящую дату: ",
                reply_markup=reg_button(user_id)
            )
        else:
            await message.answer(text="К сожалению, нет доступных дат для регистрации.")
    except gspread.exceptions.APIError as e:
        if e.response.status_code == 429:
            #wait_time = 60
            await message.answer(text=f"Превышен лимит запросов. Повторите через минуту...")
            #time.sleep(wait_time)


@router.message(F.text == ButtonText.CHECK)
async def handle_check_button(message: Message):
    try:
        user_id = message.from_user.id
        yes_button = InlineKeyboardButton(text="Да", callback_data="yes")
        no_button = InlineKeyboardButton(text="Нет", callback_data="no")
        markup = InlineKeyboardMarkup(inline_keyboard=[[yes_button, no_button]])
        if check_button(user_id):
            await message.answer(text="Вы уже зарегистрированы на игру. Хотите отменить регистрацию?",
                                 reply_markup=markup)
        else:
            await message.answer(text="Вы еще не зарегистрированы на игру.")
    except gspread.exceptions.APIError as e:
        if e.response.status_code == 429:
            #wait_time = 60
            await message.answer(text=f"Превышен лимит запросов. Повторите через минуту...")
            #time.sleep(wait_time)


@router.callback_query(F.data == "yes")
async def handle_confirm_yes(call: CallbackQuery):
    try:
        await call.message.edit_text(text="Эм, секундочку...")
        user_id = call.from_user.id
        dates = get_sheet_and_row_by_user_id(user_id)[0]
        buttons = []
        count = 0
        for date in dates:
            button = InlineKeyboardButton(text=date.title, callback_data=f"delete{count}")
            buttons.append([button])
            count += 1
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await call.message.edit_text(text="Выберите дату, регистрацию на которую вы хотите отменить: ",
                                     reply_markup=markup)
    except gspread.exceptions.APIError as e:
        if e.response.status_code == 429:
            #wait_time = 65
            await call.message.answer(text=f"Превышен лимит запросов. Повторите через минуту...")
            #time.sleep(wait_time)


@router.callback_query(lambda call: call.data.startswith("delete"))
async def handle_date_callback(call: CallbackQuery):
    try:
        await call.message.edit_text(text="Щас, секундочку...")
        user_id = call.from_user.id
        date_index = int(call.data.split("delete")[1])
        dates_to_delete, rows_to_delete = get_sheet_and_row_by_user_id(user_id)
        delete_row_and_shift_up(dates_to_delete[date_index], rows_to_delete[date_index])
        await call.message.edit_text(text="Ваша регистрация успешно удалена!")
    except gspread.exceptions.APIError as e:
        if e.response.status_code == 429:
            #wait_time = 60
            await call.message.answer(text=f"Превышен лимит запросов. Повторите через минуту...")
            #time.sleep(wait_time)


@router.callback_query(F.data == "no")
async def handle_confirm_no(call: CallbackQuery):
    await call.message.edit_text("Спасибо!", reply_markup=None)


@router.message(F.text == ButtonText.SUPPORT)
@router.message(Command("support", prefix="!/"))
async def handle_support(message: Message):
    await message.answer(text="Вы можете связаться с техподдержкой по номеру: ")
