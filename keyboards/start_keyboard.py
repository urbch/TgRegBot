from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton


class ButtonText:
    SUPPORT = "Помощь"
    REG = "Зарегистрироваться на игру"
    CHECK = "Проверить регистрацию"

def get_on_start_kb():
    button_help = KeyboardButton(text=ButtonText.SUPPORT)
    button_reg = KeyboardButton(text=ButtonText.REG)
    button_check = KeyboardButton(text=ButtonText.CHECK)
    buttons_first_row = [button_reg]
    buttons_second_row = [button_check]
    buttons_third_row = [button_help]
    markup = ReplyKeyboardMarkup(
        keyboard=[buttons_first_row, buttons_second_row, buttons_third_row],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder = "Выберите подходящий пункт:"
    )
    return markup

