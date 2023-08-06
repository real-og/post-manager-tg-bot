from loader import dp, bot, scheduler
from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta
import texts
from states import *
import logic
import keyboards as kb
import db
from handlers.users.commands import send_welcome_user



@dp.callback_query_handler(state=State.choosing_day)
async def send_channels(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(texts.choose_time, reply_markup=kb.abort_kb)
    if callback.data == 'today':
        days_to_delay = 0
    elif callback.data == 'tomorrow':
        days_to_delay = 1
    elif callback.data == 'after_tomorrow':
        days_to_delay = 2
    await state.update_data(days_to_delay=days_to_delay)
    await State.choosing_time.set()


@dp.message_handler(state=State.choosing_time)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.text == texts.abort:
        data = await state.get_data()
        message_id = data.get('message_id')
        kb_text = data.get('inline_kb_text')
        custom_kb = kb.create_user_keyboard(logic.convert_input_to_buttons(kb_text))
        await bot.copy_message(message.from_id, message.from_id, message_id, reply_markup=custom_kb)
        await message.answer(texts.confirm_message, reply_markup=kb.message_menu_kb)
        await State.confirmation_message.set()
        return
    
    try:
        hours, minutes = message.text.split(':')
    except:
        await message.answer(texts.error_time)
        return
    data = await state.get_data()
    kb_text = data.get('inline_kb_text')
    chat_id = data.get('channel_id')
    message_id = data.get('message_id')
    days_to_delay = data.get('days_to_delay')
    now = datetime.now()
    tomorrow = now + timedelta(days=days_to_delay)
    try:
        desired_time = tomorrow.replace(hour=int(hours), minute=int(minutes), second=0, microsecond=0)
    except:
        await message.answer(texts.error_time)
        return
    code = data.get('code')
    custom_kb = kb.create_user_keyboard(logic.convert_input_to_buttons(kb_text))

    if kb_text and 'https://t.me/' in kb_text:
        db.implement_usage_count_for_code(code, True)
    else:
        db.implement_usage_count_for_code(code, False)

    scheduler.add_job(logic.send_message_time, trigger='date', run_date=desired_time,
                      kwargs={'bot': bot,
                              'chat_id': chat_id,
                              'message_id': message_id,
                              'custom_kb': custom_kb, 
                              'from_id': message.from_user.id})
    await message.answer(texts.success_planned)
    await send_welcome_user(message, state)