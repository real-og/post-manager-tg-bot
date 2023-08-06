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

@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    filters.Text(equals=texts.create_code_btn, ignore_case=True),
                    state=State.admin_menu)
async def send_channels(message: types.Message, state: FSMContext):
    channels = db.get_channels()
    await message.answer(texts.choose_to_create_code, reply_markup=kb.generate_channel_kb(channels))
    await State.choosing_to_create_code.set()



@dp.callback_query_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    state=State.choosing_to_create_code)
async def send_channels(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'cancel':
        await callback.message.answer(texts.admin_welcome, reply_markup=kb.admin_menu_kb)
        await State.admin_menu.set()
        return
    id = callback.data
    if id != '0':
        try: 
            chat = await bot.get_chat(id)
            await state.update_data(channel_id=id)
        except:
            await callback.message.answer(texts.error_bot_rights)
            return
    
    await state.update_data(channel_id=id)
    await callback.message.answer(texts.choose_code_days, reply_markup=kb.abort_kb)
    await State.choosing_days_of_code.set()


@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    state=State.choosing_days_of_code)
async def send_channels(message: types.Message, state: FSMContext):
    days = message.text
    if not days.isdecimal():
        await message.answer(texts.error_number_expected)
        return
    if int(message.text) > 90:
        await message.answer(texts.error_day_amount_too_much)
        return
    await state.update_data(day_amount=message.text)
    await message.answer(texts.choose_post_whole_amount)
    await State.choosing_all_post_number.set()


@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    state=State.choosing_all_post_number)
async def send_channels(message: types.Message, state: FSMContext):
    all_post_number = message.text
    if not all_post_number.isdecimal():
        await message.answer(texts.error_number_expected)
        return
    if int(message.text) > 1000:
        await message.answer(texts.error_post_amount_too_much)
        return
    await state.update_data(all_post_amount=message.text)
    await message.answer(texts.choose_post_tg_amount)
    await State.choosing_tg_post_number.set()


@dp.message_handler(filters.IDFilter(chat_id=ADMIN_IDS),
                    state=State.choosing_tg_post_number)
async def send_channels(message: types.Message, state: FSMContext):
    tg_post_number = message.text
    if not tg_post_number.isdecimal():
        await message.answer(texts.error_number_expected)
        return
    if int(message.text) > 1000:
        await message.answer(texts.error_post_amount_too_much)
        return
    code = logic.generate_random_code(14)
    data = await state.get_data()
    channel_id = data.get('channel_id')
    day_amount = data.get('day_amount')
    all_post_number = data.get('all_post_amount')
    if channel_id is None:
        await message.answer(texts.error_channel_id)
        return
    db.add_code(code, channel_id, day_amount, all_post_number, tg_post_number)
    name = db.get_channel_name_by_id(channel_id).get('name')
    await message.answer(texts.success_added_code(code, channel_id, day_amount, all_post_number, tg_post_number, name), reply_markup=kb.admin_menu_kb)
    await State.admin_menu.set()

    
    
    