import requests
import time
from insta_db import BotBase


def check_new_comments(_access_token, base: BotBase):
    """Функция проверяет наличие новых комментариев"""
    while True:
        com_start = time.time()
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
                                print(f'New comment: {comment["text"]} from {com_info.json()["from"]["username"]}')
                            else:
                                pass
                        except KeyError:
                            base.add_new_comment(com_info.json()['id'])

        finish_com = time.time() - com_start
        print(f'Comments need: {finish_com}')
        time.sleep(300)
        print('\nNew cycle comments\n')
