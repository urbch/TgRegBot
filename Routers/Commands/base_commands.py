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
        text=f"""Здравствуйте, {markdown.hbold(message.from_user.full_name)}!
                   Выберите подходящий пункт в меню""",
        reply_markup=get_on_start_kb()
    )


@router.message(Command("help"))
async def process_help(message: Message):
    text = "Данный бот предназначен для регистрации участников квизов на викторины"
    await message.answer(text=text)


@router.message(F.text == ButtonText.REG)
async def handle_reg_button(message: Message):
    date1 = InlineKeyboardButton(text="1")
    date2 = InlineKeyboardButton(text="2")
    date3 = InlineKeyboardButton(text="3")
    row1 = [date1]
    row2 = [date2]
    row3 = [date3]
    rows = [row1, row2, row3]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await message.amswer(
        text="Выберите подохдящую дату: ",
        reply_markup=markup,
    )


@router.message(Command("support", prefix="!/"))
async def handle_support(message: Message):
    tg_channel_button = InlineKeyboardButton(text="Канал в телеграме",
                                             url="https://skillbox.ru/media/code/biblioteka-matplotlib-dlya-postroeniya-grafikov")
    row = [tg_channel_button]
    rows = [row]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await message.answer(
        text="Ссылки и прочие ресурсы",
        reply_markup=markup,
    )
