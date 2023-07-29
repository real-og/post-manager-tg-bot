from loader import dp, bot, ADMIN_IDS
from aiogram import types
from states import *
from aiogram.dispatcher import FSMContext
import texts
from aiogram.dispatcher import filters
import keyboards as kb
import db

@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    commands=['add_channel'],
                    state='*')
async def send_channels(message: types.Message, state: FSMContext):
    await message.answer(texts.resend_message, reply_markup=kb.abort_kb)
    await State.waiting_message_from_channels.set()


@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    state=State.waiting_message_from_channels)
async def send_channels(message: types.Message, state: FSMContext):
    print(message)
    if message.text == texts.abort:
        await state.reset_state()
        await message.answer(texts.success)
    elif message.forward_from_chat:
        await state.reset_state()
        db.add_channel(message.forward_from_chat.id, message.forward_from_chat.title)
        await message.answer(texts.success_added)
    else:
        await message.answer(texts.error_forwarded)
