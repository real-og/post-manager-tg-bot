from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
import texts
from states import *
import logic
import keyboards as kb
from handlers.users.commands import send_welcome_user
import db
from datetime import datetime, timedelta


@dp.callback_query_handler(state=State.user_menu)
async def send_channels(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'enter':
        await callback.message.answer(texts.enter_code_short, reply_markup=kb.abort_kb)
        await State.entering_code.set()
    else:
        code_info = db.get_codes_and_channels([callback.data])[0]
        
        if (datetime.now() - code_info['creation_datetime'] > timedelta(days=code_info['limit_days']) and code_info['limit_days'] != 0) or \
           (code_info['usage_count'] >= code_info['limit_count_all'] and code_info['limit_count_all'] != 0):
            await callback.message.answer('Время либо количество постов израсходовано. Код будет удален из активированных')
            data = await state.get_data()
            user_codes = data.get('user_codes')
            user_codes.remove(code_info['code'])
            await state.update_data(user_codes=user_codes)
            await state.update_data(inline_kb_text=None)
            if user_codes is None:
                await state.update_data(user_codes=[])
            await callback.message.answer(texts.enter_code, reply_markup=kb.create_user_menu(user_codes))
            await State.user_menu.set()          
            return
            
        await callback.message.answer(texts.generate_success_code(code_info), reply_markup=kb.create_post_kb)
        await State.user_code_view.set()



@dp.message_handler(state=State.entering_code)
async def send_welcome(message: types.Message, state: FSMContext):
    input = message.text

    if input == texts.abort:
        await send_welcome_user(message, state)
        return
    
    code = logic.check_access_code(input)
    if code is None:
        await message.answer(texts.error_code)
    else:
        await state.update_data(channel_id=code['channel_id'])
        await state.update_data(code=code['code'])
        await message.answer(texts.generate_success_code(code))
        data = await state.get_data()
        user_codes = data.get('user_codes')
        user_codes.append(code['code'])
        await state.update_data(user_codes=user_codes)
        await send_welcome_user(message, state)
        