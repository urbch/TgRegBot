import logging

from aiogram import Bot, Dispatcher
from Routers import router as main_router

import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
dp.include_router(main_router)

#def check_date:
#   return dates[]

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    dp.run_polling(bot)


