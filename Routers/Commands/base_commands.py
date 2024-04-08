from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, CallbackQuery
from aiogram.utils import markdown

from keyboards.start_keyboard import ButtonText, get_on_start_kb

router = Router(name=__name__)


class Registration(StatesGroup):
    date_selection = State()
    team_name = State()
    team_size = State()
    leader_name = State()
    phone_number = State()


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
    date1 = InlineKeyboardButton(text="02.02.24", callback_data="date02.02.24")
    date2 = InlineKeyboardButton(text="03.03.24", callback_data="date03.03.24")
    date3 = InlineKeyboardButton(text="04.04.24", callback_data="date04.04.24")
    row1 = [date1]
    row2 = [date2]
    row3 = [date3]
    rows = [row1, row2, row3]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    await message.answer(
        text="Выберите подохдящую дату: ",
        reply_markup=markup,
    )


@router.callback_query(lambda call: call.data.startswith("date"))


async def handle_date_callback(call: CallbackQuery, state: FSMContext):
    selected_date = call.data.split("date")[1]
    try:
        await call.answer(text=f"Вы выбрали дату: {selected_date}")
        await call.message.edit_text(text=f"Вы выбрали дату: {selected_date}", reply_markup=None)
        await state.update_data(selected_date=selected_date)
        await state.set_state(Registration.team_name)
        await call.message.answer(text="Введите название вашей команды:")
    except Exception as e:
        await call.answer(text="Ошибка обработки даты")


@router.message(Registration.team_name, F.text)
async def handle_team_name(message: types.Message, state: FSMContext):
        await state.update_data(team_name=message.text)
        await state.clear()
        await message.answer(text=f"Название вашей команды: {message.text}")


@router.message(Registration.team_name)
async def handle_team_name_invalid_type(message: types.Message):
    await message.answer(text="Неверный тип данных. Попробуйте еще раз: ")


class IsNumber(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.text.isdigit()


@router.message(Registration.team_size, F)
async def handle_team_name(message: types.Message, state: FSMContext):
        await state.update_data(team_name=message.text)
        await state.clear()
        await message.answer(text=f"Название вашей команды: {message.text}")


@router.message(Registration.team_size)
async def handle_team_name_invalid_type(message: types.Message):
    await message.answer(text="Неверный тип данных. Попробуйте еще раз: ")


@router.message(F.text == ButtonText.CHECK)
async def handle_check_button(message: Message):
    await message.answer(text="Вы еще не зарегистрированы ни на одну игру")


@router.message(F.text == ButtonText.SUPPORT)
@router.message(Command("support", prefix="!/"))
async def handle_support(message: Message):
    await message.answer(text="Вы можете связаться с техподдержкой по номеру: 89116546555")
