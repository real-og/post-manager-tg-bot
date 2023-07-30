from loader import dp, bot, ADMIN_IDS
from aiogram import types
from states import *
from aiogram.dispatcher import FSMContext
import texts
from aiogram.dispatcher import filters
import keyboards as kb
import db

@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    commands=['delete_channel'],
                    state='*')
async def send_channels(message: types.Message, state: FSMContext):
    channels = db.get_channels()
    await message.answer(texts.delete_channels, reply_markup=kb.generate_channel_kb(channels))
    await State.deleting_channel.set()

@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    filters.Text(equals=texts.delete_channel_btn, ignore_case=True),
                    state=State.admin_menu)
async def send_channels(message: types.Message, state: FSMContext):
    channels = db.get_channels()
    await message.answer(texts.delete_channels, reply_markup=kb.generate_channel_kb(channels))
    await State.deleting_channel.set()



@dp.callback_query_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    state=State.deleting_channel)
async def send_channels(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'cancel':
        await callback.message.answer(texts.admin_welcome, reply_markup=kb.admin_menu_kb)
        await State.admin_menu.set()
        return
    id = callback.data
    db.delete_channel(id)
    await callback.message.answer(texts.success_deleted)
    await callback.message.answer(texts.admin_welcome, reply_markup=kb.admin_menu_kb)
    await State.admin_menu.set()
    



