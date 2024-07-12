import os
from telebot.types import Message, CallbackQuery
from .keyborads import main_menu, msg_list, msg_editor
from configuration import bot


file_path_for_edit = ''

@bot.callback_query_handler(func=lambda call: call.data == 'back')
@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    """Запуск интерфейса в телеграмме"""
    text = 'Выберете команду:'
    bot.send_message(message.from_user.id, text=text, reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: call.data == 'get_points')
def get_ig_user_points(call):
    """Стартует вывод накопленных очков пользователя по юзернэйму"""
    bot.answer_callback_query(call.id)
    bot.set_state(user_id=call.from_user.id, state='get_points')
    bot.send_message(chat_id=call.from_user.id, text='Введите username пользователя:')


@bot.callback_query_handler(func=lambda call: call.data == 'get_msg_text')
def get_msg_text(call: CallbackQuery):
    """Выводим список доступных сообщений"""
    bot.answer_callback_query(call.id)
    bot.send_message(chat_id=call.from_user.id, text='Выберете сообщение для просмотра:', reply_markup=msg_list())


@bot.callback_query_handler(func=lambda call: call.data.startswith('view'))
def get_message(call: CallbackQuery):
    """Выводим содержание соответствующего файла"""
    bot.answer_callback_query(call.id)
    file_path = os.path.join('msg_text', call.data.replace('view_', ''))
    with open(file_path, 'r', encoding='utf-8') as file:
        bot.send_message(chat_id=call.from_user.id, text=file.read())
        bot.send_message(chat_id=call.from_user.id, text='Выберете сообщение для просмотра:', reply_markup=msg_list())


@bot.callback_query_handler(func=lambda call: call.data == 'edit_msg_text')
def get_msg_list_for_editor(call: CallbackQuery):
    """Выводим список сообщений для редактирования"""
    bot.answer_callback_query(call.id)
    bot.send_message(chat_id=call.from_user.id, text='Выберете сообщение для редактирования:', reply_markup=msg_editor())


@bot.callback_query_handler(func=lambda call: call.data.startswith('edit'))
def start_edit_message(call: CallbackQuery):
    """Запускаем редактирование сообщения"""
    global file_path_for_edit
    print(file_path_for_edit)
    bot.answer_callback_query(call.id)
    file_path_for_edit = call.data.replace('edit_', '')
    bot.send_message(chat_id=call.from_user.id, text='Введите новый текст сообщения:')
    bot.set_state(user_id=call.from_user.id, state='edit_msg')


@bot.message_handler(state='edit_msg')
def edit_msg_text(message: Message):
    """Меняем старый текст сообщения на новый прямо в файле"""
    global file_path_for_edit
    print(file_path_for_edit)
    with open(os.path.join('msg_text', file_path_for_edit), 'w', encoding='utf-8') as file:
        file.write(message.text)

    bot.send_message(chat_id=message.from_user.id, text='Сообщение изменено!')
    bot_start(message)
