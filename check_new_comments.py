import random
from instagrapi import Client
from insta_db import BotBase
from sending_message_for_bot import send_message
from asyncio import sleep
import aiohttp


async def check_new_comments(_access_token, base: BotBase, client: Client):
    """Функция проверяет наличие новых комментариев"""
    while True:
        # Получаем все отработанные комментарии
        old_comments = base.get_old_comments()

        # Запрашиваем все медиа которые есть на аккаунте
        media_url = f'https://graph.facebook.com/v20.0/17841454901909441/media?limit=300&access_token={_access_token}'
        async with aiohttp.ClientSession() as session:
            media_response = await (await session.get(media_url)).json()

        # Проходимся по каждой и смотрим наличие комментариев
        for media in media_response['data']:

            url = f'https://graph.facebook.com/v20.0/{media["id"]}/comments?access_token={_access_token}'
            async with aiohttp.ClientSession() as session:
                response = await (await session.get(url)).json()

                # Если комментарии есть, то проверяем новые они или нет
                if len(response['data']) > 0:

                    for comment in response['data']:

                        if comment["id"] not in old_comments:
                            com_url = f'https://graph.facebook.com/v20.0/{comment["id"]}?fields=from&access_token={_access_token}'
                            async with aiohttp.ClientSession() as session_2:
                                com_info = await (await session_2.get(com_url)).json()
                            base.add_new_comment(com_info.json()['id'])

                            try:
                                if com_info.json()["from"]["username"] != '20.10.body.lab.studio':
                                    user_id = int(client.user_id_from_username(com_info.json()["from"]["username"]))
                                    await send_message(
                                        user_id=user_id,
                                        action='comment',
                                        client=client,
                                        base=base
                                    )
                                else:
                                    pass
                            except KeyError:
                                base.add_new_comment(com_info.json()['id'])

        await sleep(random.randint(60, 120))
