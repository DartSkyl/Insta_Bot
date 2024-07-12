import requests
import time
import random
from instagrapi import Client
from insta_db import BotBase
from sending_message_for_bot import send_message


def check_new_comments(_access_token, base: BotBase, client: Client):
    """Функция проверяет наличие новых комментариев"""
    while True:
        # Получаем все отработанные комментарии
        old_comments = base.get_old_comments()

        # Запрашиваем все медиа которые есть на аккаунте
        media_url = f'https://graph.facebook.com/v20.0/17841454901909441/media?limit=300&access_token={_access_token}'
        media_response = requests.get(url=media_url).json()

        # Проходимся по каждой и смотрим наличие комментариев
        for media in media_response['data']:

            url = f'https://graph.facebook.com/v20.0/{media["id"]}/comments?access_token={_access_token}'
            response = requests.get(url=url)

            # Если комментарии есть, то проверяем новые они или нет
            if len(response.json()['data']) > 0:

                for comment in response.json()['data']:

                    if comment["id"] not in old_comments:
                        com_url = f'https://graph.facebook.com/v20.0/{comment["id"]}?fields=from&access_token={_access_token}'
                        com_info = requests.get(url=com_url)
                        base.add_new_comment(com_info.json()['id'])

                        try:
                            if com_info.json()["from"]["username"] != '20.10.body.lab.studio':
                                user_id = int(client.user_id_from_username(com_info.json()["from"]["username"]))
                                send_message(
                                    user_id=user_id,
                                    action='comment',
                                    client=client,
                                    base=base
                                )
                            else:
                                pass
                        except KeyError:
                            base.add_new_comment(com_info.json()['id'])

        time.sleep(random.randint(60, 120))
