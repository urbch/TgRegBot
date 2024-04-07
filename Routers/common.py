from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from keyboards.start_keyboard import ButtonText

router = Router(name=__name__)

@router.message()
async def process_message(message: Message):
    await message.answer(
        text="К сожалению, я Вас не понимаю. Выберите пункт из меню."
    )
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("К сожалению, я Вас не понимаю. Выберите пункт из меню")
