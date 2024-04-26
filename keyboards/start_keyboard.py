from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton


class ButtonText:
    SUPPORT = "Помощь"
    REG = "Зарегистрироваться на игру"
    CHECK = "Проверить регистрацию"

def get_on_start_kb():
    button_help = KeyboardButton(text=ButtonText.SUPPORT)
    button_reg = KeyboardButton(text=ButtonText.REG)
    button_check = KeyboardButton(text=ButtonText.CHECK)
    markup = ReplyKeyboardMarkup(
        keyboard=[[button_reg], [button_check], [button_help]],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder = "Выберите подходящий пункт:"
    )
    return markup

