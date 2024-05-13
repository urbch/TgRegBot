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

max_team_size = 10

# Открываем таблицу
sheet = gc.open_by_key(SHEET_ID)
worksheet = sheet.sheet1


def reg_button(user_id):
    dates_data = worksheet.get_all_records()
    registered_dates = []
    dates = [row["Date"] for row in dates_data]
    for sheet_name in sheet.worksheets():  # Проверяем каждую страницу
        if sheet_name.title in dates:  # Проверяем, что страница соответствует дате
            worksheet2 = sheet.worksheet(sheet_name.title)
            cell = worksheet2.find(str(user_id))  # Ищем ID пользователя
            if cell:
                registered_dates.append(sheet_name.title)  # Добавляем дату, если ID найден
    available_dates = [
        row["Date"]
        for row in dates_data
        if row.get("DateInfo", "").lower() != "full" and row["Date"] not in registered_dates
    ]
    buttons = []
    for date in available_dates:
        time_address = worksheet.cell(worksheet.find(date).row, worksheet.find("Time&Address").col).value
        button = InlineKeyboardButton(text=date, callback_data=f"date{date}time_address{time_address}")
        buttons.append([button])
    if not available_dates:
        return False
    else:
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        return markup


@router.callback_query(lambda call: call.data.startswith("date"))
async def handle_date_callback(call: CallbackQuery, state: FSMContext):
    selected_date = call.data.split("date")[1].split("time_address")[0]
    selected_time = call.data.split("date")[1].split("time_address")[1]
    try:
        ##await call.answer(text=f"Вы выбрали дату: {selected_date}")
        await call.message.edit_text(text=f"""Вы выбрали дату: {selected_date}
Время и место проведения: {selected_time}""", reply_markup=None)
        yes_button = InlineKeyboardButton(text="Да", callback_data="confirm_yes_date")
        no_button = InlineKeyboardButton(text="Нет", callback_data="confirm_no_date")
        markup = InlineKeyboardMarkup(inline_keyboard=[[yes_button, no_button]])
        await call.message.answer(text="Вы уверены, что хотите записаться на эту дату? ", reply_markup=markup)
        await state.update_data(selected_date=selected_date)
    except Exception as e:
        await call.answer(text="Ошибка обработки даты")

@router.callback_query(F.data == "confirm_yes_date")
async def handle_confirm_yes_date(call: CallbackQuery, state: FSMContext):
    await state.set_state(TeamInfo.team_name)
    await call.message.edit_text(text="Введите название вашей команды:")


@router.callback_query(F.data == "confirm_no_date")
async def handle_confirm_no_date(call: CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    await call.message.edit_text(text="Выберите подходящую дату: ", reply_markup=reg_button(user_id))


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
    if number <= max_team_size and number > 1:
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
    await call.message.edit_text(text="Минуточку плюс секундочку...")
    user_id = call.from_user.id
    user_name = call.from_user.username
    if not user_name:
        user_name = "NO USERNAME"
    # Получаем данные из state
    data = await get_data(state)
    new_row = [user_id, user_name, data[1], data[2], data[3], data[4]]
    worksheet2 = sheet.worksheet(data[0])
    worksheet2.append_row(new_row)
    if len(worksheet2.get_all_records()) == max_team_size:
        date_cell = worksheet.find(data[0])
        worksheet.update_cell(date_cell.row, 2, "full")
    await call.message.edit_text("Ваша заявка принята!", reply_markup=None)
    await state.clear()


async def get_data(state: FSMContext):
    data = await state.get_data()
    date = data.get("selected_date")
    team_name = data.get("team_name")
    team_size = data.get("team_size")
    leader_name = data.get("leader_name")
    phone_number = data.get("phone_number")
    data_array = [date, team_name, team_size, leader_name, phone_number]
    return data_array


@router.callback_query(F.data == "confirm_no")
async def handle_confirm_no(call: CallbackQuery):
    user_id = call.from_user.id
    await call.message.edit_text(f"""Пожалуйста, начните регистрацию заново.
Выберите подохдящую дату: """, reply_markup=reg_button(user_id))


async def send_user_info(state: FSMContext) -> str:
    data = await get_data(state)
    text = f"""Проверьте информацию:
Дата участия: {data[0]}
Название команды: {data[1]}
Количество участников: {data[2]}
Капитан команды: {data[3]}
Ваш контактный номер: {data[4]}
Информация верна?"""
    return text


def check_button(user_id):
    dates_data = worksheet.get_all_records()
    dates = [row["Date"] for row in dates_data]
    for sheet_name in sheet.worksheets():  # Проверяем каждую страницу
        if sheet_name.title in dates:  # Проверяем, что страница соответствует дате
            worksheet2 = sheet.worksheet(sheet_name.title)
            cell = worksheet2.find(str(user_id))  # Ищем ID пользователя
            if cell:
                return True
    return False


def delete_row_and_shift_up(worksheet_name, row_index):
    """Удаляет строку из Google Таблицы и сдвигает остальные строки вверх."""
    # Получаем количество строк в таблице
    num_rows = len(worksheet_name.get_all_values())

    # Проверяем, существует ли строка с указанным индексом
    if 1 <= row_index <= num_rows:
        # Удаляем строку
        worksheet_name.delete_rows(row_index)
    else:
        print(f"Ошибка: Индекс строки {row_index} вне диапазона.")


def get_sheet_and_row_by_user_id(user_id):
    """Находит лист и номер строки, где находится указанный ID пользователя."""
    registred_woksheets = []
    rows_to_delete = []
    for sheet_name in sheet.worksheets():  # Проверяем каждую страницу
        worksheet4 = sheet.worksheet(sheet_name.title)
        cell = worksheet4.find(str(user_id))  # Ищем ID пользователя
        if cell:
            registred_woksheets.append(worksheet4)
            rows_to_delete.append(cell.row)
    return registred_woksheets, rows_to_delete  # Если ID не найден, возвращаем None, None
