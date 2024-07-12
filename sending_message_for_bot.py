from instagrapi import Client
from insta_db import BotBase
import os
import time


mes_dict = {
    'rules': os.path.join('msg_text', 'rules.txt'),
    'stop': os.path.join('msg_text', 'stop.txt'),
    'reaction': os.path.join('msg_text', '1_point.txt'),
    'comment': os.path.join('msg_text', '2_point.txt'),
    'mention': os.path.join('msg_text', '5_point.txt')
}

action_dict = {
    'reaction': 1,
    'comment': 2,
    'mention': 5
}


def send_message(user_id: int, action: str, client: Client, base: BotBase):
    """Функция отвечает за отправку сообщений. Отправляемое сообщение зависит от задействованного сценария"""
    stop_list = base.get_stop_list()
    if str(user_id) not in stop_list:
        if action != 'bonus':

            with open(f'{mes_dict[action]}', 'r', encoding='utf-8') as file:
                msg_text = file.read()
                client.direct_send(text=msg_text, user_ids=[user_id])

                if action in ['reaction', 'comment', 'mention']:
                    base.add_points(str(user_id), action_dict[action])

                elif action == 'stop':
                    base.add_in_stop_list(str(user_id))

        else:
            user_points = base.get_user_points(str(user_id))
            msg_text = f'На данный момент ваш счет составляет {user_points[0]}' if user_points \
                else f'У вас пока что нет очков! Что бы узнать подробности акции отправьте "ПРАВИЛА"'
            client.direct_send(text=msg_text, user_ids=[user_id])

    else:
        pass

