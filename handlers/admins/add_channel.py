from loader import dp, bot, ADMIN_IDS
from aiogram import types
from states import *
from aiogram.dispatcher import FSMContext
import texts
from aiogram.dispatcher import filters
import keyboards as kb
import db



@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    filters.Text(equals=texts.add_channel_btn, ignore_case=True),
                    state=State.admin_menu)
async def send_channels(message: types.Message, state: FSMContext):
    await message.answer(texts.resend_message, reply_markup=kb.abort_kb)
    await State.waiting_message_from_channels.set()


@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    commands=['add_channel'],
                    state='*')
async def send_channels(message: types.Message, state: FSMContext):
    await message.answer(texts.resend_message, reply_markup=kb.abort_kb)
    await State.waiting_message_from_channels.set()


@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    state=State.waiting_message_from_channels,
                    content_types=types.ContentType.ANY)
async def send_channels(message: types.Message, state: FSMContext):
    if message.text == texts.abort:
        await message.answer(texts.admin_welcome, reply_markup=kb.admin_menu_kb)
        await State.admin_menu.set()
    elif message.forward_from_chat:
        db.add_channel(message.forward_from_chat.id, message.forward_from_chat.title)
        await message.answer(texts.success_added)
        await message.answer(texts.admin_welcome, reply_markup=kb.admin_menu_kb)
        await State.admin_menu.set()
    else:
        await message.answer(texts.error_forwarded)
