import concurrent.futures
from instagrapi import Client
from configuration import *
from check_new_comments import check_new_comments
from direct_monitoring import direct_monitoring
from insta_db import BotBase


cl = Client()
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

bot_base = BotBase()
bot_base.check_db_structure()


def comments_checking():
    check_new_comments(ACCESS_TOKEN, bot_base)


def direct_watcher():
    direct_monitoring(cl, bot_base)


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(comments_checking)
        future2 = executor.submit(direct_watcher)

    concurrent.futures.wait([future1, future2])
