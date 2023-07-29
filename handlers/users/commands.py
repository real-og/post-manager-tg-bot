from loader import dp, scheduler, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
import texts
from states import *
from logic import send_message_time
from datetime import datetime, timedelta

@dp.message_handler(commands=['start'], state="*")
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(texts.enter_code)
    await State.entering_code.set()


