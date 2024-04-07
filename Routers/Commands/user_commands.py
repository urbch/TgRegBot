from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.start_keyboard import ButtonText

router = Router(name=__name__)



@router.message(F.text == ButtonText.REG)
@router.message(Command("showdate"))
async def handle_command_show_date(message: Message):

    text = ("Вот список доступных дат для записи, выберите подходящую: "
            )
    await message.answer(text = text)
