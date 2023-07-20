from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
import texts
from states import *
import logic
import keyboards as kb


@dp.message_handler(state=State.typing_message)
async def send_welcome(message: types.Message, state: FSMContext):
    message_to_send = await message.send_copy(message.from_id)
    message_id = message_to_send.message_id
    await state.update_data(message_id=message_id)
    await message.answer(texts.confirm_message, reply_markup=kb.yes_no_kb)
    await State.confirmation_message.set()


@dp.message_handler(state=State.confirmation_message)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.text == texts.yes:
        data = await state.get_data()
        chat_id = data.get('channel_id')
        message_id = data.get('message_id')
        await bot.copy_message(chat_id, message.from_id, message_id)
    elif message.text == texts.no:
        await message.answer(texts.abort)
        await message.answer(texts.enter_code)
        await State.entering_code.set()
    else:
        await message.answer(texts.use_kb)
    

