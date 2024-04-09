from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import markdown

from Routers.Commands.reg_handler import reg_button
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
    await message.answer(
        text="Выберите подохдящую дату: ",
        reply_markup=reg_button()
    )

@router.message(F.text == ButtonText.CHECK)
async def handle_check_button(message: Message):
    await message.answer(text="Вы еще не зарегистрированы ни на одну игру")

@router.message(F.text == ButtonText.SUPPORT)
@router.message(Command("support", prefix="!/"))
async def handle_support(message: Message):
    await message.answer(text="Вы можете связаться с техподдержкой по номеру: 89116546555")
