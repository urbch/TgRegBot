import re
from aiogram import types


def validate_phone_number(message: types.Message) -> bool:
    pattern = re.compile(r'^\+7\d{10}$|^8\d{10}$|^9\d{9}$')
    if pattern.match(message.text):
        return True
    else:
        return False


