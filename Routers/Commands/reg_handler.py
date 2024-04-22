from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import markdown
from validators.phone_number_validator import validate_phone_number
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os


router = Router(name=__name__)


class TeamInfo(StatesGroup):
    selected_date = State()
    team_name = State()
    team_size = State()
    leader_name = State()
    phone_number = State()
    report = State()


KEY_FILE_LOCATION = 'tg-bot-421112-4814e071cafa.json'
SHEET_ID="12rKgsq0zUmgP2lykXcpry9KuUmmTzj18qRGYE_pjdbM"

# Аутентификация с помощью API ключа
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, scope)
gc = gspread.authorize(creds)

# Открываем таблицу
sheet = gc.open_by_key(SHEET_ID)

# Выбираем нужный лист (по умолчанию первый)
worksheet = sheet.sheet1

# Пример: чтение данных из таблицы
data = worksheet.get_all_records()


def reg_button():
    date1 = InlineKeyboardButton(text=data[0].get("Date"), callback_data=f"date{data[0].get("Date")}")
    date2 = InlineKeyboardButton(text=data[1].get("Date"), callback_data=f"date{data[1].get("Date")}")
    date3 = InlineKeyboardButton(text=data[2].get("Date"), callback_data=f"date{data[2].get("Date")}")
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
        ##await call.answer(text=f"Вы выбрали дату: {selected_date}")
        await call.message.edit_text(text=f"Вы выбрали дату: {selected_date}", reply_markup=None)
        await state.update_data(selected_date=selected_date)
        await state.set_state(TeamInfo.team_name)
        await call.message.answer(text="Введите название вашей команды:")
    except Exception as e:
        await call.answer(text="Ошибка обработки даты")


@router.message(TeamInfo.team_name, F.text)
async def handle_team_name(message: types.Message, state: FSMContext):
    await state.update_data(team_name=message.text)
    #await message.answer(text=f"Название вашей команды: {message.text}")
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
        #await message.answer(text=f"Число участников: {message.text}")
        await state.set_state(TeamInfo.leader_name)
        await message.answer(text="Введите имя капитана команды:")
    else:
        await message.answer(text="Число участников не должно превышать 10. Попробуйте еще раз")


@router.message(TeamInfo.team_size)
async def handle_team_size_non_digit(message: types.Message):
    await message.answer(text="Неверный тип данных. Попробуйте еще раз")


@router.message(TeamInfo.leader_name, F.text)
async def handle_leader_name(message: types.Message, state: FSMContext):
    await state.update_data(leader_name=message.text)
    #await message.answer(text=f"Имя капитана команды: {message.text}")
    await state.set_state(TeamInfo.phone_number)
    await message.answer(text="Введите контакный номер телефона:")


@router.message(TeamInfo.leader_name)
async def handle_leader_name_invalid_type(message: types.Message):
    await message.answer(text="Неверный тип данных. Попробуйте еще раз")


@router.message(TeamInfo.phone_number, validate_phone_number)
async def handle_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    #await message.answer(text=f"Ваш контактный номер телефона: {message.text}")
    await state.set_state(TeamInfo.report)
    yes_button = InlineKeyboardButton(text="Да", callback_data="confirm_yes")
    no_button = InlineKeyboardButton(text="Нет", callback_data="confirm_no")
    markup = InlineKeyboardMarkup(inline_keyboard=[[yes_button, no_button]])
    await message.answer(text=await send_user_info(state), reply_markup=markup)
    #await state.clear()


@router.message(TeamInfo.phone_number)
async def handle_invalid_phone_number(message: types.Message):
    await message.answer(text="Введите корректный номер телефона")


@router.callback_query(F.data == "confirm_yes")
async def handle_confirm_yes(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    # Получаем данные из state
    data = await state.get_data()
    date = data.get("selected_date")
    team_name = data.get("team_name")
    team_size = data.get("team_size")
    leader_name = data.get("leader_name")
    phone_number = data.get("phone_number")
    new_row = [user_id, team_name, team_size, leader_name, phone_number]
    worksheet2 = sheet.worksheet(date)
    worksheet2.append_row(new_row)
    await call.message.edit_text("Ваша заявка принята!", reply_markup=None)
    await state.clear()


@router.callback_query(F.data == "confirm_no")
async def handle_confirm_no(call: CallbackQuery):
    await call.message.edit_text(f"""Пожалуйста, начните регистрацию заново.
Выберите подохдящую дату: """, reply_markup=reg_button())


async def send_user_info(state: FSMContext) -> str:
    data = await state.get_data()
    date = data.get("selected_date")
    team_name = data.get("team_name")
    team_size = data.get("team_size")
    leader_name = data.get("leader_name")
    phone_number = data.get("phone_number")

    text = f"""Проверьте информацию:
Дата участия: {date}
Название команды: {team_name}
Количество участников: {team_size}
Капитан команды: {leader_name}
Ваш контактный номер: {phone_number}
Информация верна?"""
    return text


def check_button(user_id):
    for sheet_name in [data[0].get("Date"), data[1].get("Date"), data[2].get("Date")]:
        worksheet3 = sheet.worksheet(sheet_name)
        cell = worksheet3.find(str(user_id))
        if cell:
            return True
    return False





