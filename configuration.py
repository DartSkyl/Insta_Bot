import os
from dotenv import load_dotenv, find_dotenv
import logging

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()


ACCOUNT_USERNAME = os.getenv('ACCOUNT_USERNAME')
ACCOUNT_PASSWORD = os.getenv('ACCOUNT_PASSWORD')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

# logging.basicConfig(
#     filename='instagram_bot.log',
#     filemode='a',
#     format="%(asctime)s %(levelname)s %(message)s"
# )
# logging.getLogger().setLevel(logging.ERROR)
