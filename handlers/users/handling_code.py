from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
import texts
from states import *
import logic
import keyboards as kb
from handlers.users.commands import send_welcome_user


@dp.callback_query_handler(state=State.user_menu)
async def send_channels(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'enter':
        await callback.message.answer(texts.enter_code, reply_markup=kb.abort_kb)
        await State.entering_code.set()


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
        

