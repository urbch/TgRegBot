from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils import markdown

from validators.phone_numder_validator import validate_phone_number

router = Router(name=__name__)


class TeamInfo(StatesGroup):
    selected_date = State()
    team_name = State()
    team_size = State()
    leader_name = State()
    phone_number = State()


def reg_button():
    date1 = InlineKeyboardButton(text="02.02.24", callback_data="date02.02.24")
    date2 = InlineKeyboardButton(text="03.03.24", callback_data="date03.03.24")
    date3 = InlineKeyboardButton(text="04.04.24", callback_data="date04.04.24")
    row1 = [date1]
    row2 = [date2]
    row3 = [date3]
    rows = [row1, row2, row3]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup


@router.callback_query(lambda call: call.data.startswith("date"))
async def handle_date_callback(call: CallbackQuery, state: FSMContext):
    selected_date = call.data.split("date")[1]
    try:
        await call.answer(text=f"Вы выбрали дату: {selected_date}")
        await call.message.edit_text(text=f"Вы выбрали дату: {selected_date}", reply_markup=None)
        await state.update_data(selected_date=selected_date)
        await state.set_state(TeamInfo.team_name)
        await call.message.answer(text="Введите название вашей команды:")
    except Exception as e:
        await call.answer(text="Ошибка обработки даты")


@router.message(TeamInfo.team_name, F.text)
async def handle_team_name(message: types.Message, state: FSMContext):
    await state.update_data(team_name=message.text)
    await message.answer(text=f"Название вашей команды: {message.text}")
    await state.set_state(TeamInfo.team_size)
    await message.answer(text="Введите число участников команды:")


@router.message(TeamInfo.team_name)
async def handle_team_name_invalid_type(message: types.Message):
    await message.answer(text="Неверный тип данных. Попробуйте еще раз")


@router.message(TeamInfo.team_size, F.text.isdigit())
async def handle_team_size(message: types.Message, state: FSMContext):
    number = int(message.text)
    if number <= 10 and number > 0:
        await state.update_data(team_size=message.text)
        await message.answer(text=f"Число участников: {message.text}")
        await state.set_state(TeamInfo.leader_name)
        await message.answer(text="Введите имя капитана команды:")
    else:
        await message.answer(text="Число участников не должно превышать 10. Попробуйте еще раз")


@router.message(TeamInfo.team_size)
async def handle_team_size_non_digit(message: types.Message):
    await message.answer(text="Неверный тип данных. Попробуйте еще раз")


@router.message(TeamInfo.leader_name, F.text)
async def handle_leader_name(message: types.Message, state: FSMContext):
    await state.update_data(team_name=message.text)
    await message.answer(text=f"Имя капитана команды: {message.text}")
    await state.set_state(TeamInfo.phone_number)
    await message.answer(text="Введите контакный номер телефона:")


@router.message(TeamInfo.leader_name)
async def handle_leader_name_invalid_type(message: types.Message):
    await message.answer(text="Неверный тип данных. Попробуйте еще раз")


@router.message(TeamInfo.phone_number, validate_phone_number)
async def handle_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.clear()
    await message.answer(text=f"Ваш контактный номер телефона: {message.text}")


@router.message(TeamInfo.phone_number)
async def handle_invalid_phone_number(message: types.Message):
    await message.answer(text="Введите корректный номер телефона")


async def send_user_info(state: FSMContext) -> str:
    data = await state.get_data()
    team_name = data.get("team_name")
    team_size = data.get("team_size")
    leader_name = data.get("leader_name")
    phone_number = data.get("phone_number")
    text = markdown.text("Проверьте информацию:", markdown.text("Название команды: ", team_name),
                         markdown.text("Количество участников: ", team_size),
                         markdown.text("Капитан команды: ", leader_name),
                         markdown.text("Ваш контактный номер: ", phone_number, "",
                         "Пожалуйста скажите что вы не ошиблись с вводом"))
    return text
