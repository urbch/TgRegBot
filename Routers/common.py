from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from keyboards.start_keyboard import ButtonText

router = Router(name=__name__)

@router.message(F.text == ButtonText.BYE)
async def handle_bye_message(mesage: Message):
    await mesage.answer(
        text="See you later, click /start any time!",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message()
async def process_message(message: Message):

    await message.answer(
        text = "Wait a second..."
    )
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Something new...")
