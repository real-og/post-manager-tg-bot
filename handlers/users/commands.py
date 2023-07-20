from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
import texts
from states import *

@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(texts.enter_code)
    await State.entering_code.set()

