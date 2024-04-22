import logging
import os


from aiogram import Bot, Dispatcher
from Routers import router as main_router
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()
dp.include_router(main_router)


#def check_date:
#   return dates[]

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    dp.run_polling(bot)


