from instagrapi import Client
from insta_db import BotBase
import os
import datetime


mes_dict = {
    'rules': os.path.join('msg_text', 'rules.txt'),
    'stop': os.path.join('msg_text', 'stop.txt'),
    'reaction': os.path.join('msg_text', '1_point.txt'),
    'comment': os.path.join('msg_text', '2_point.txt'),
    'mention': os.path.join('msg_text', '5_point.txt'),
    'return': os.path.join('msg_text', 'return.txt')
}

action_dict = {
    'reaction': 1,
    'comment': 2,
    'mention': 5
}

# В этом словаре будет храниться информация от том, кто сколько сегодня активничал,
# так как у нас максимум 3 активности в день
today_user_actions_dict = dict()


async def send_message(user_id: int, action: str, client: Client, base: BotBase):
    """Функция отвечает за отправку сообщений. Отправляемое сообщение зависит от задействованного сценария"""
    stop_list = base.get_stop_list()
    if str(user_id) not in stop_list:
        if action != 'bonus':

            with open(f'{mes_dict[action]}', 'r', encoding='utf-8') as file:
                msg_text = file.read()
                client.direct_send(text=msg_text, user_ids=[user_id])

                if action in ['reaction', 'comment', 'mention']:

                    # Ниже идущая конструкция if else нужна для ограничения пользователей
                    # в активности до 3 трех раз в день

                    key = str(datetime.date.today())  # Основной ключ это текущая дата
                    user = str(user_id)  # Вложенный ключ это ID пользователя инстаграм

                    # Проверяем, есть ли сегодняшний ключ
                    if today_user_actions_dict.get(key):

                        # Проверяем был ли активен сегодня данный пользователь
                        if today_user_actions_dict[key].get(user):

                            # Если был активен, то смотрим, что бы активностей было меньше 3
                            if today_user_actions_dict[key][user] < 3:
                                today_user_actions_dict[key][user] += 1
                                base.add_points(str(user_id), action_dict[action])

                            # Иначе сообщаем о том, что он достиг лимита
                            else:
                                msg_text = 'На сегодня вы достигли лимита активности!'
                                client.direct_send(text=msg_text, user_ids=[user_id])

                        # Если этот пользователь сегодня активен первый раз, то добавляем его
                        # в словарь под ключем сегодняшней даты и ключем его собственного ID
                        else:
                            today_user_actions_dict[key][user] = 1
                            base.add_points(str(user_id), action_dict[action])

                    # Если это первая активность за сегодня, то добавляем ключ
                    # сегодняшней даты и сразу под ним пользователя
                    else:
                        today_user_actions_dict[key] = {user: 1}
                        base.add_points(str(user_id), action_dict[action])

                elif action == 'stop':
                    base.add_in_stop_list(str(user_id))

        else:
            user_points = base.get_user_points(str(user_id))
            msg_text = f'На данный момент ваш счет составляет {user_points[0]} балов' if user_points \
                else f'У вас пока что нет очков! Что бы узнать подробности акции отправьте "ПРАВИЛА"'
            client.direct_send(text=msg_text, user_ids=[user_id])

    elif action == 'return':
        base.remove_from_stop_list(str(user_id))
        with open(f'{mes_dict[action]}', 'r', encoding='utf-8') as file:
            msg_text = file.read()
            client.direct_send(text=msg_text, user_ids=[user_id])

