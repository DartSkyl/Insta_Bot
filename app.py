import concurrent.futures
import datetime
from instagrapi import Client
from instagrapi.exceptions import UserNotFound
from configuration import *
from check_new_comments import check_new_comments
from direct_monitoring import direct_monitoring
from insta_db import BotBase

from tg_interface import handlers  # noqa
from telebot import custom_filters
from telebot.types import Message, BotCommand


cl = Client()
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)


def comments_checking():
    check_new_comments(ACCESS_TOKEN, bot_base, cl)


def direct_watcher():
    direct_monitoring(cl, bot_base)


def start_tg_interface():
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )

    bot.add_custom_filter(custom_filters.StateFilter(bot))
    for admin in ADMINS:
        bot.send_message(chat_id=admin, text='Бот запущен')
    bot.infinity_polling(skip_pending=True)


bot_base = BotBase()
bot_base.check_db_structure()


# Данную функцию пришлось вынести сюда, так как для ее использования нужен client,
# а импортировать его мы не можем так как возникнет циркулярный импорт

@bot.message_handler(state='get_points')
def output_user_points(message: Message):
    """Выводим очки пользователя"""
    if message.from_user.id in ADMINS:
        bot.send_message(chat_id=message.from_user.id, text='Немного подождите...')
        try:
            user_id = cl.user_id_from_username(username=message.text)
            points = bot_base.get_user_points(user_id)[0]
            text = f'У пользователя {message.text} {points} очков'
            bot.send_message(chat_id=message.from_user.id, text=text)
            bot.set_state(user_id=message.from_user.id, state=0)  # И так сойдет
        except UserNotFound:
            text = 'Ошибка при вводе username пользователя!'
            bot.send_message(chat_id=message.from_user.id, text=text)
            bot.set_state(user_id=message.from_user.id, state=0)
        except TypeError:
            text = f'У пользователя {message.text} 0 очков'
            bot.send_message(chat_id=message.from_user.id, text=text)
            bot.set_state(user_id=message.from_user.id, state=0)
        handlers.bot_start(message)


if __name__ == '__main__':
    print('Стартуем')
    # start_tg_interface()
    with open('bonus_bot.log', 'a') as log_file:
        log_file.write(f'\n\n\n========== New bot session {datetime.datetime.now()} ==========\n\n\n')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(comments_checking)
        future2 = executor.submit(direct_watcher)
        future3 = executor.submit(start_tg_interface)

    concurrent.futures.wait([future1, future2, future3])
