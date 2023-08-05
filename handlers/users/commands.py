from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
import texts
from states import *
import keyboards as kb

@dp.message_handler(commands=['start'], state="*")
async def send_welcome_user(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_codes = data.get('user_codes')
    if user_codes is None:
        await state.update_data(user_codes=[])
    await message.answer(texts.enter_code, reply_markup=kb.create_user_menu(user_codes))
    await State.user_menu.set()


