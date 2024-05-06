from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from Routers.Commands.reg_handler import reg_button, check_button
from keyboards.start_keyboard import ButtonText, get_on_start_kb

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
    if reg_button() != False:
        await message.answer(
            text="Выберите подохдящую дату: ",
            reply_markup=reg_button()
        )
    else:
        await message.answer(text="К сожалению, нет доступных дат для регистрации.")


@router.message(F.text == ButtonText.CHECK)
async def handle_check_button(message: Message):
    user_id = message.from_user.id
    yes_button = InlineKeyboardButton(text="Да", callback_data="yes")
    no_button = InlineKeyboardButton(text="Нет", callback_data="no")
    markup = InlineKeyboardMarkup(inline_keyboard=[[yes_button, no_button]])
    if check_button(user_id):
        await message.answer(text="Вы уже зарегистрированы на игру. Хотите зарегистрироваться еще раз?", reply_markup=markup)
    else:
        await message.answer(text="Вы еще не зарегистрированы на игру. Хотите зарегистрироваться?", reply_markup=markup)


@router.callback_query(F.data == "yes")
async def handle_confirm_yes(call: CallbackQuery):
    if reg_button() != False:
        await call.message.edit_text(
            text="Выберите подохдящую дату: ",
            reply_markup=reg_button()
        )
    else:
        await call.message.edit_text(text="К сожалению, нет доступных дат для регистрации.")


@router.callback_query(F.data == "no")
async def handle_confirm_no(call: CallbackQuery):
    await call.message.edit_text("Спасибо!", reply_markup=None)


@router.message(F.text == ButtonText.SUPPORT)
@router.message(Command("support", prefix="!/"))
async def handle_support(message: Message):
    await message.answer(text="Вы можете связаться с техподдержкой по номеру: ")
