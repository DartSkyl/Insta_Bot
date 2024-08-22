import os
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from .keyborads import main_menu, msg_list, msg_editor
from configuration import bot, dp, ADMINS


file_path_for_edit = ''


class AdminStates(StatesGroup):
    get_points = State()
    edit_message = State()
    password = State()


@dp.message(Command("start"))
async def bot_start(message: Message, bot_msg=False):
    """Запуск интерфейса в телеграмме"""
    if message.from_user.id in ADMINS or bot_msg:
        text = 'Выберете команду:'
        await message.answer(text=text, reply_markup=main_menu())


@dp.callback_query(F.data == 'back')
async def back(call: CallbackQuery):
    await call.answer()
    await bot_start(call.message, True)


@dp.callback_query(F.data == 'get_points')
async def get_ig_user_points(call: CallbackQuery, state: FSMContext):
    """Стартует вывод накопленных очков пользователя по юзернэйму"""
    if call.from_user.id in ADMINS:
        await call.answer()
        await state.set_state(AdminStates.get_points)
        await call.message.answer('Введите username пользователя:')


@dp.callback_query(F.data == 'get_msg_text')
async def get_msg_text(call: CallbackQuery):
    """Выводим список доступных сообщений"""
    if call.from_user.id in ADMINS:
        await call.answer()
        await call.message.answer(text='Выберете сообщение для просмотра:', reply_markup=msg_list())


@dp.callback_query(F.data.startswith('view'))
async def get_message(call: CallbackQuery):
    """Выводим содержание соответствующего файла"""
    if call.from_user.id in ADMINS:
        await call.answer()
        file_path = os.path.join('msg_text', call.data.replace('view_', ''))
        with open(file_path, 'r', encoding='utf-8') as file:
            await call.message.answer(text=file.read())
            await call.message.answer(text='Выберете сообщение для просмотра:', reply_markup=msg_list())


@dp.callback_query(F.data == 'edit_msg_text')
async def get_msg_list_for_editor(call: CallbackQuery):
    """Выводим список сообщений для редактирования"""
    if call.from_user.id in ADMINS:
        await call.answer()
        await call.message.answer(text='Выберете сообщение для редактирования:', reply_markup=msg_editor())


@dp.callback_query(F.data.startswith('edit'))
async def start_edit_message(call: CallbackQuery, state: FSMContext):
    """Запускаем редактирование сообщения"""
    if call.from_user.id in ADMINS:
        global file_path_for_edit
        await call.answer()
        file_path_for_edit = call.data.replace('edit_', '')
        await call.message.answer(text='Введите новый текст сообщения:')
        await state.set_state(AdminStates.edit_message)


@dp.message(AdminStates.edit_message)
async def edit_msg_text(message: Message):
    """Меняем старый текст сообщения на новый прямо в файле"""
    if message.from_user.id in ADMINS:
        global file_path_for_edit
        with open(os.path.join('msg_text', file_path_for_edit), 'w', encoding='utf-8') as file:
            file.write(message.text)
        await message.answer('Сообщение изменено!')
        await bot_start(message)


@dp.message(Command("new_password"))
async def change_password(message: Message, state: FSMContext):
    """Инициируем смену пароля от инстаграм аккаунта"""
    if message.from_user.id in ADMINS:
        await state.set_state(AdminStates.password)
        await message.answer('Введите новый пароль:')


@dp.message(AdminStates.password)
async def set_new_password_and_bot_restart(message: Message):
    """Меняем пароль и перезапускаем бота"""
    if message.from_user.id in ADMINS:
        new_pass = message.text

        with open('.env', 'r') as file:
            old_data = file.read()
            old_pass = old_data.splitlines()[1]

        new_data = old_data.replace(old_pass, f"ACCOUNT_PASSWORD = '{new_pass}'")

        with open('.env', 'w') as file:
            file.write(new_data)

        await message.answer('Пароль изменен, перезапускаю бота...')
        os.system('systemctl restart bonus_bot.service')
