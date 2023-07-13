from loader import dp, bot, ADMIN_IDS
from aiogram import types
from states import *
from aiogram.dispatcher import FSMContext
import texts
from aiogram.dispatcher import filters
import keyboards as kb


@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    commands=['admin'],
                    state='*')
async def send_welcome_admin(message: types.Message, state: FSMContext):
    await message.answer(texts.admin_welcome)


@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    commands=['my_channels'],
                    state='*')
async def send_channels(message: types.Message, state: FSMContext):
    await message.answer(texts.admin_welcome)
