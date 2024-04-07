from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from keyboards.start_keyboard import ButtonText, get_on_start_kb

router = Router(name=__name__)

@router.message()
async def process_message(message: Message):
    await message.answer(
        text="К сожалению, я Вас не понимаю. Выберите пункт из меню."
    )
