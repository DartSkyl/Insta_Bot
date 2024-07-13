from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    inline_markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='Посмотреть балы по username', callback_data='get_points'),
        InlineKeyboardButton(text='Посмотреть текст сообщений', callback_data='get_msg_text'),
        InlineKeyboardButton(text='Редактировать текст сообщений', callback_data='edit_msg_text')
    ]

    inline_markup.add(*buttons)
    return inline_markup


def msg_list():
    inline_markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='Правила', callback_data='view_rules.txt'),
        InlineKeyboardButton(text='За реакцию', callback_data='view_1_point.txt'),
        InlineKeyboardButton(text='За комментарий', callback_data='view_2_point.txt'),
        InlineKeyboardButton(text='За упоминание в истории', callback_data='view_5_point.txt'),
        InlineKeyboardButton(text='Рейтинг', callback_data='view_return.txt'),
        InlineKeyboardButton(text='Стоп', callback_data='view_stop.txt'),
        InlineKeyboardButton(text='⏪ Назад', callback_data='back')
    ]

    inline_markup.add(*buttons)
    return inline_markup


def msg_editor():
    inline_markup = InlineKeyboardMarkup(row_width=1)
    buttons = [
        InlineKeyboardButton(text='Правила', callback_data='edit_rules.txt'),
        InlineKeyboardButton(text='За реакцию', callback_data='edit_1_point.txt'),
        InlineKeyboardButton(text='За комментарий', callback_data='edit_2_point.txt'),
        InlineKeyboardButton(text='За упоминание в истории', callback_data='edit_5_point.txt'),
        InlineKeyboardButton(text='Рейтинг', callback_data='edit_return.txt'),
        InlineKeyboardButton(text='Стоп', callback_data='edit_stop.txt'),
        InlineKeyboardButton(text='⏪ Назад', callback_data='back')
    ]

    inline_markup.add(*buttons)
    return inline_markup
