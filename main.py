from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import executor
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery

from sqlite import add_message, on_start, print_messages, delete_message_from_db, add_message_prem

from config import Token, admin_ids, prem_users_ids

# Создаем объект бота и передаем в него наш токен
bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())


class AddMessage(StatesGroup):
    wait_for_message = State()


# Обработчик для команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    if user_id in admin_ids:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_add_message = types.KeyboardButton(text='Рассказать анекдот')
        button_view_all = types.KeyboardButton(text='Посмотреть все')
        keyboard.add(button_add_message, button_view_all)
        await message.answer(
            'Привет! Чтобы рассказать уморительный анекдот админу используй команду /add_anecdot или кнопку "Рассказать анекдот". Для просмотра всех сообщений используй команду /view_all или кнопку "Посмотреть все".',
            reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_add_message = types.KeyboardButton(text='Рассказать анекдот')
        keyboard.add(button_add_message)
        await message.answer(
            'Привет! Чтобы рассказать уморительный анекдот админу используй команду /add_anecdot или кнопку "Рассказать анекдот"',
            reply_markup=keyboard)


# Обработчик для кнопки "Добавить сообщение" и для команды /add_message
@dp.message_handler(commands=['add_anecdot'])
@dp.message_handler(Text(equals='Рассказать анекдот'))
async def add_message_button_handler(message: types.Message):
    await AddMessage.wait_for_message.set()
    await message.answer('Введи свой невероятно смешной анекдот', reply_markup=types.ReplyKeyboardRemove())


# Обработчик для ввода сообщения пользователем
@dp.message_handler(state=AddMessage.wait_for_message)
async def process_user_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    user_message = message.text
    if user_message:
        if user_id in prem_users_ids:
            add_message_prem(username, user_message)
            await message.reply('Успешно! Админ точно надорвет животик от смеха')
            if user_id in admin_ids:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_add_message = types.KeyboardButton(text='Рассказать анекдот')
                button_view_all = types.KeyboardButton(text='Посмотреть все')
                keyboard.add(button_add_message, button_view_all)
                await message.answer(
                    'Чтобы рассказать уморительный анекдот админу используй команду /add_anecdot или кнопку "Рассказать анекдот". Для просмотра всех сообщений используй команду /view_all или кнопку "Посмотреть все".',
                    reply_markup=keyboard)
            else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_add_message = types.KeyboardButton(text='Рассказать анекдот')
                keyboard.add(button_add_message)
                await message.answer(
                    'Ты можешь отправить еще один анекдот, нажав на кнопку',
                    reply_markup=keyboard)
        elif add_message(username, user_message):
            await message.reply('Успешно! Админ точно надорвет животик от смеха')
            if user_id in admin_ids:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_add_message = types.KeyboardButton(text='Рассказать анекдот')
                button_view_all = types.KeyboardButton(text='Посмотреть все')
                keyboard.add(button_add_message, button_view_all)
                await message.answer(
                    'Чтобы рассказать уморительный анекдот админу используй команду /add_anecdot или кнопку "Рассказать анекдот". Для просмотра всех сообщений используй команду /view_all или кнопку "Посмотреть все".',
                    reply_markup=keyboard)
            else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_add_message = types.KeyboardButton(text='Рассказать анекдот')
                keyboard.add(button_add_message)
                await message.answer(
                    'Ты можешь отправить еще один анекдот, нажав на кнопку',
                    reply_markup=keyboard)
        else:
            await message.reply(
                'Дошутился! Ты достиг лимита отправки сообщений (10). Подожди, пока админ посмеется над каждым, и сможешь отправлять снова!')
            if user_id in admin_ids:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_add_message = types.KeyboardButton(text='Рассказать анекдот')
                button_view_all = types.KeyboardButton(text='Посмотреть все')
                keyboard.add(button_add_message, button_view_all)
                await message.answer(
                    'Чтобы рассказать уморительный анекдот админу используй команду /add_anecdot или кнопку "Рассказать анекдот". Для просмотра всех сообщений используй команду /view_all или кнопку "Посмотреть все".',
                    reply_markup=keyboard)
            else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                button_add_message = types.KeyboardButton(text='Рассказать анекдот')
                keyboard.add(button_add_message)
                await message.answer(
                    'Ты сможешь отправить еще один анекдот попозже, нажав на кнопку',
                    reply_markup=keyboard)
    else:
        await message.reply('Анекдот не может быть пустым! Не над чем ржакать')

    await state.finish()


@dp.message_handler(text='Посмотреть все')
@dp.message_handler(commands=['view_all'])
async def view_all_messages(message: types.Message):
    user_id = message.from_user.id
    if user_id in admin_ids:
        result = print_messages()

        if result:
            for row in result:
                username = row[1]
                user_mes = row[2]
                keyboard = InlineKeyboardMarkup()  # Создаем InlineKeyboardMarkup

                delete_button = InlineKeyboardButton(text='Удалить', callback_data=f'delete_message_{row[0]}')
                keyboard.add(delete_button)  # Добавляем кнопку "Удалить" в InlineKeyboardMarkup

                await bot.send_message(chat_id=message.from_user.id, text=f"Анекдот от @{username}:\n\n{user_mes}",
                                       reply_markup=keyboard)

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_add_message = types.KeyboardButton(text='Рассказать анекдот')
        keyboard.add(button_add_message)
        await message.answer(
            'Тебе не доступна эта команда! Чтобы рассказать уморительный анекдот админу используй команду /add_anecdot или кнопку "Рассказать анекдот"',
            reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith('delete_message_'))
async def delete_message_callback(callback_query: CallbackQuery):
    message_id = int(callback_query.data.split('_')[2])
    await delete_message_from_db(message_id)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    # await bot.send_message(chat_id=callback_query.from_user.id, text='Сообщение удалено!')


@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    user_id = message.from_user.id
    if user_id in admin_ids:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_add_message = types.KeyboardButton(text='Рассказать анекдот')
        button_view_all = types.KeyboardButton(text='Посмотреть все')
        keyboard.add(button_add_message, button_view_all)
        await message.answer(
            'Чтобы рассказать уморительный анекдот админу используй команду /add_anecdot или кнопку "Рассказать анекдот". Для просмотра всех сообщений используй команду /view_all или кнопку "Посмотреть все".',
            reply_markup=keyboard)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_add_message = types.KeyboardButton(text='Рассказать анекдот')
        keyboard.add(button_add_message)
        await message.answer(
            'Чтобы рассказать уморительный анекдот админу используй команду /add_anecdot или кнопку "Рассказать анекдот"',
            reply_markup=keyboard)


# Оборачиваем диспетчер хендлером в декоратор, внутри которого будет асинхронная функция, принимающая все текстовые сообщения и отправляющая их обратно
@dp.message_handler()
async def echo_message(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)


# Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_start())
