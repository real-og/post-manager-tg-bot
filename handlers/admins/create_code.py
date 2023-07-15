from loader import dp, bot, ADMIN_IDS
from aiogram import types
from states import *
from aiogram.dispatcher import FSMContext
import texts
from aiogram.dispatcher import filters
import keyboards as kb
import db
import logic

@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    commands=['create_code'],
                    state='*')
async def send_channels(message: types.Message, state: FSMContext):
    channels = db.get_channels()
    await message.answer(texts.choose_to_create_code, reply_markup=kb.generate_channel_kb(channels))
    await State.choosing_to_create_code.set()


@dp.callback_query_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    state=State.choosing_to_create_code)
async def send_channels(callback: types.CallbackQuery, state: FSMContext):
    id = callback.data
    try: 
        chat = await bot.get_chat(id)
        await state.update_data(channel_id=id)
    except:
        await callback.message.answer(texts.error_bot_rights)
        return
    await state.update_data(channel_id=id)
    await callback.message.answer(texts.choose_code_type, reply_markup=kb.code_types_kb)
    await State.choosing_type_of_code.set()


@dp.callback_query_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    state=State.choosing_type_of_code)
async def send_channels(callback: types.CallbackQuery, state: FSMContext):
    type = callback.data
    code = logic.generate_random_code(14)
    data = await state.get_data()
    channel_id = data.get('channel_id')
    if channel_id is None:
        await callback.message.answer(texts.error_channel_id)
        return
    await callback.message.answer(texts.success_added_code(code, channel_id, type))
    db.add_code(code, type, channel_id)

    
    
    