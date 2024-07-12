from instagrapi import Client
from insta_db import BotBase
from sending_message_for_bot import send_message
import time
import random


stop_list = []

action_dict = {
    'правила': 'rules',
    'стоп': 'stop',
    'бонус': 'bonus'
}


def direct_monitoring(client: Client, base: BotBase):
    """Функция проверят директ инстаграм на наличие целевых действий,
    а именно упоминание в истории, реакция на историю и слов БОНУС, СТОП, ПРАВИЛА"""

    while True:
        mes_start = time.time()
        old_messages = base.get_old_messages()
        # Все переписки проверять смысла нет, по этому будем проверять только последние 10
        user_chats = client.direct_threads()[:10]

        # Пройдемся по каждому чату и проверим последние 10 сообщений на нужные нам
        for chat in user_chats:

            # Берем каждое отдельное сообщение
            for msg in chat.messages[:10]:

                #  Смотрим что бы оно не принадлежало нам и не было уже обработано 54875534063
                if msg.user_id != '54875534063' and msg.id not in old_messages:

                    if msg.item_type == 'xma_reel_mention':  # Упоминание в истории
                        print(f'Упоминание в истории от {msg.user_id}')

                        send_message(
                            user_id=int(msg.user_id),
                            action='mention',
                            client=client,
                            base=base
                        )

                    elif msg.item_type == 'xma_reel_share' and len(msg.text) == 1:  # Реакция на историю
                        print(f'Реакция на историю от {msg.user_id}')

                        send_message(
                            user_id=int(msg.user_id),
                            action='reaction',
                            client=client,
                            base=base
                        )

                    try:
                        if msg.text.lower() in ['бонус', 'стоп', 'правила']:
                            print(f'Пользователь хочет "{msg.text}"')
                            send_message(
                                user_id=int(msg.user_id),
                                action=action_dict[msg.text.lower()],
                                client=client,
                                base=base
                            )

                    except AttributeError:
                        pass

                    base.add_new_message(msg.id)

        mes_finish = time.time() - mes_start
        print(f'Messages need: {mes_finish}')
        time.sleep(random.randint(540, 900))
        print('\nNew cycle direct\n')
