from loader import dp, bot, ADMIN_IDS
from aiogram import types
from states import *
from aiogram.dispatcher import FSMContext
import texts
from aiogram.dispatcher import filters
import keyboards as kb
import db
chat_id = -1001611331902

@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    commands=['admin'],
                    state='*')
async def send_welcome_admin(message: types.Message, state: FSMContext):
    await message.answer(texts.admin_welcome, reply_markup=kb.admin_menu_kb)
    await State.admin_menu.set()



@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    filters.Text(equals=texts.channels_btn, ignore_case=True),
                    state=State.admin_menu)
async def send_added_channels(message: types.Message, state: FSMContext):
    channels = db.get_channels()
    await message.answer(texts.your_channels, reply_markup=kb.generate_channel_kb(channels))
    await message.answer(texts.instruction_to_get_menu, reply_markup=kb.admin_menu_kb)
    await State.admin_menu.set()



@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    commands=['my_channels'],
                    state='*')
async def send_added_channels(message: types.Message, state: FSMContext):
    channels = db.get_channels()
    await message.answer(texts.your_channels, reply_markup=kb.generate_channel_kb(channels))
    await message.answer(texts.instruction_to_get_menu, reply_markup=kb.admin_menu_kb)
    await State.admin_menu.set()

