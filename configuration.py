import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()


ACCOUNT_USERNAME = os.getenv('ACCOUNT_USERNAME')
ACCOUNT_PASSWORD = os.getenv('ACCOUNT_PASSWORD')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMINS = [int(i) for i in os.getenv('ADMINS').split()]

DEFAULT_COMMANDS = (
    ("start", "Главное меню и рестарт"),
    ("new_password", "Смена пароля"),
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

logging.basicConfig(
    filename='bonus_bot.log',
    filemode='a',
    format="%(asctime)s %(levelname)s %(message)s"
)
logging.getLogger().setLevel(logging.ERROR)
