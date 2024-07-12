import sqlite3


class BotBase:
    """Класс для реализации базы данных и методов для взаимодействия с ней"""

    @staticmethod
    def check_db_structure():
        """Создаем при первом подключении, а в последующем проверяем, таблицы необходимые для работы бота"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            # Таблица со всеми участниками
            cursor.execute('CREATE TABLE IF NOT EXISTS Users (user_id TEXT PRIMARY KEY, points INTEGER);')

            # Таблица отработанных комментариев
            cursor.execute('CREATE TABLE IF NOT EXISTS Old_comments (comment_id TEXT);')

            # Таблица отработанных сообщений
            cursor.execute('CREATE TABLE IF NOT EXISTS Old_messages (message_id TEXT);')

            # Таблица с теми кто отказался от участия
            cursor.execute('CREATE TABLE IF NOT EXISTS Stop_list (user_id TEXT);')

            connection.commit()

    @staticmethod
    def add_new_comment(comment_id: str):
        """Записываем новый комментарий к отработанным"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'INSERT INTO Old_comments (comment_id) VALUES ("{comment_id}");')
            connection.commit()

    @staticmethod
    def add_new_message(message_id: str):
        """Записываем новый комментарий к отработанным"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'INSERT INTO Old_messages (message_id) VALUES ("{message_id}");')
            connection.commit()

    @staticmethod
    def add_points(user_id: str, points: int):
        """Добавляем очки пользователю, если пользователя еще нет в базе, то записываем"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'INSERT INTO Users (user_id, points) VALUES ("{user_id}", {points + 7})'
                           f'ON CONFLICT (user_id)'
                           f'DO UPDATE SET points = Users.points + {points};')
            connection.commit()

    @staticmethod
    def add_in_stop_list(user_id: str):
        """Добавляем в стоп-лист"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'INSERT INTO Stop_list (user_id) VALUES ("{user_id}");')
            connection.commit()

    @staticmethod
    def get_stop_list():
        """Достаем всех, кто отказался от участия"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            all_users = cursor.execute(f'SELECT * FROM Stop_list;').fetchall()
            all_users = [i[0] for i in all_users]  # Так как возвращается список картежей
            return set(all_users)

    @staticmethod
    def get_old_comments():
        """Выдаем все отработанные комментарии для сверки"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            all_comments = cursor.execute(f'SELECT * FROM Old_comments;').fetchall()
            all_comments = [i[0] for i in all_comments]  # Так как возвращается список картежей
            return set(all_comments)

    @staticmethod
    def get_old_messages():
        """Выдаем все отработанные сообщения для сверки"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            all_messages = cursor.execute(f'SELECT * FROM Old_messages;').fetchall()
            all_messages = [i[0] for i in all_messages]  # Так как возвращается список картежей
            return set(all_messages)

    @staticmethod
    def get_user_points(user_id: str):
        """Возвращаем очки конкретного пользователя"""
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            user_points = cursor.execute(f'SELECT points FROM Users WHERE user_id = "{user_id}";').fetchone()
            return user_points


