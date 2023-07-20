from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
import texts
from states import *
import logic

@dp.message_handler(state=State.entering_code)
async def send_welcome(message: types.Message, state: FSMContext):
    code = message.text
    channel_id = logic.check_access_code(code)

    if channel_id is None:
        await message.answer(texts.error_code)
    else:
        await message.answer(texts.success_code)
        await State.typing_message.set()

