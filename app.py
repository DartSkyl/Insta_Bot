import concurrent.futures
import datetime
import asyncio
from instagrapi import Client
from instagrapi.exceptions import UserNotFound
from configuration import *
from check_new_comments import check_new_comments
from direct_monitoring import direct_monitoring
from insta_db import BotBase
from aiogram.types.bot_command import BotCommand
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F

from tg_interface import handlers  # noqa


cl = Client()
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)


async def comments_checking():
    await check_new_comments(ACCESS_TOKEN, bot_base, cl)


async def direct_watcher():
    await direct_monitoring(cl, bot_base)


async def start_tg_interface():
    await bot.set_my_commands(
        commands=[
            BotCommand(command='start', description='Главное меню или рестарт'),
            BotCommand(command='new_password', description='Смена пароля от аккаунта')
        ]
    )

    for admin in ADMINS:
        await bot.send_message(chat_id=admin, text='Бот запущен')

    await dp.start_polling(bot)


bot_base = BotBase()
bot_base.check_db_structure()


# Данную функцию пришлось вынести сюда, так как для ее использования нужен client,
# а импортировать его мы не можем так как возникнет циркулярный импорт

@dp.message(handlers.AdminStates.get_points)
async def output_user_points(message: Message, state: FSMContext):
    """Выводим очки пользователя"""
    if message.from_user.id in ADMINS:
        await message.answer('Немного подождите...')
        try:
            user_id = cl.user_id_from_username(username=message.text)
            points = bot_base.get_user_points(user_id)[0]
            text = f'У пользователя {message.text} {points} очков'
            await message.answer(text)
            await state.clear()
        except UserNotFound:
            text = 'Ошибка при вводе username пользователя!'
            await message.answer(text)
        except TypeError:
            text = f'У пользователя {message.text} 0 очков'
            await message.answer(text)
        await state.clear()
        await handlers.bot_start(message)


async def start_up():
    task_1 = asyncio.create_task(start_tg_interface())
    task_2 = asyncio.create_task(comments_checking())
    task_3 = asyncio.create_task(direct_watcher())
    with open('bonus_bot.log', 'a') as log_file:
        log_file.write(f'\n\n\n========== New bot session {datetime.datetime.now()} ==========\n\n\n')
    await asyncio.gather(task_1, task_2, task_3)

# if __name__ == '__main__':
#     print('Стартуем')
#     # start_tg_interface()
    with open('bonus_bot.log', 'a') as log_file:
        log_file.write(f'\n\n\n========== New bot session {datetime.datetime.now()} ==========\n\n\n')
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         future1 = executor.submit(comments_checking)
#         future2 = executor.submit(direct_watcher)
#         future3 = executor.submit(start_tg_interface)
#
#     concurrent.futures.wait([future1, future2, future3])

if __name__ == '__main__':
    try:
        asyncio.run(start_up())
    except KeyboardInterrupt:
        print('Хорош, бро')
