from loader import dp, bot, ADMIN_IDS
from aiogram import types
from states import *
from aiogram.dispatcher import FSMContext
import texts
from aiogram.dispatcher import filters
import keyboards as kb
import db

@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    commands=['create_code'],
                    state='*')
async def send_channels(message: types.Message, state: FSMContext):
    channels = db.get_channels()
    await message.answer(texts.choose_to_create_code, reply_markup=kb.generate_channel_kb(channels))
    await State.choosing_to_create_code.set()


@dp.callback_query_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    state=State.deleting_channel)
async def send_channels(callback: types.CallbackQuery, state: FSMContext):
    id = callback.data
    try: 
        chat = await bot.get_chat(id)
        state.update_data(channel_id=id)
    except:
        await callback.answer(texts.error_bot_rights)
        return
    state.update_data(channel_id=id)
    await callback.answer(texts.choose_code_type, reply_markup=kb.code_types_kb)
    await State.choosing_type_of_code()
    
    