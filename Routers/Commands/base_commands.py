from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import markdown

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
    date1 = InlineKeyboardButton(text="1",
                                 url="https://ru.freepik.com/free-photo/kitty-with-monochrome-wall-behind-her_13863370.htm#query=%D0%BA%D0%BE%D1%82&position=0&from_view=keyword&track=ais&uuid=48b7a3b0-7cb5-49d4-9211-b13e75adc8e6")
    date2 = InlineKeyboardButton(text="2",
                                 url="https://ru.freepik.com/free-photo/adorable-looking-kitten-with-yarn_72412955.htm#query=%D0%BA%D0%BE%D1%82&position=1&from_view=keyword&track=ais&uuid=48b7a3b0-7cb5-49d4-9211-b13e75adc8e6")
    date3 = InlineKeyboardButton(text="3",
                                 url="https://ru.freepik.com/free-photo/closeup-vertical-shot-of-a-cute-european-shorthair-cat_13828199.htm#query=%D0%BA%D0%BE%D1%82&position=2&from_view=keyword&track=ais&uuid=48b7a3b0-7cb5-49d4-9211-b13e75adc8e6")
    row1 = [date1]
    row2 = [date2]
    row3 = [date3]
    rows = [row1, row2, row3]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await message.answer(
        text="Выберите подохдящую дату: ",
        reply_markup=markup,
    )


@router.message(F.text == ButtonText.SUPPORT)
@router.message(Command("support", prefix="!/"))
async def handle_support(message: Message):
    await message.answer(text="Вы можете связаться с техподдержкой по номеру: 89116546555")
