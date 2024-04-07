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
        text = f"Привет, {markdown.hbold(message.from_user.full_name)}!",
        parse_mode=ParseMode.HTML,
        reply_markup=get_on_start_kb()
    )
@router.message(F.text == ButtonText.WHATS_NEXT)
@router.message(Command("help"))
async def process_help(message: Message):
    text = markdown.text(
        markdown.markdown_decoration.quote("I'm a test bot."),
        markdown.text(
            "Send me",
            markdown.markdown_decoration.bold(
                markdown.text(
                    markdown.underline("literally"),
                     "any",
                 ),
            ),
            markdown.markdown_decoration.quote("message!"),
        ),
        sep="\n",
    )
    await message.answer(text = text, parse_mode = ParseMode.MARKDOWN_V2)

@router.message(Command("info", prefix="!/"))
async def handle_info(message: Message):
    tg_channel_button = InlineKeyboardButton(text="Канал в телеграме",
                                             url="https://skillbox.ru/media/code/biblioteka-matplotlib-dlya-postroeniya-grafikov")
    row = [tg_channel_button]
    rows = [row]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await message.answer(
        text="Ссылки и прочие ресурсы",
        reply_markup=markup,
    )
