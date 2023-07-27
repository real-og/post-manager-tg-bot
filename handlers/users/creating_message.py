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
    await message.answer(texts.confirm_message, reply_markup=kb.message_menu_kb)
    await State.confirmation_message.set()


@dp.callback_query_handler(state=State.confirmation_message)
async def send_channels(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'finish':
        data = await state.get_data()
        kb_text = data.get('inline_kb_text')
        chat_id = data.get('channel_id')
        message_id = data.get('message_id')
        custom_kb = kb.create_user_keyboard(logic.convert_input_to_buttons(kb_text))
        await bot.copy_message(chat_id, callback.from_user.id, message_id, reply_markup=custom_kb)
        await callback.message.answer(texts.success_posted)
        await bot.send_message()
    elif callback.data == 'buttons':
        await callback.message.answer(texts.instruction_for_buttons)
        await State.adding_buttons.set()


@dp.message_handler(state=State.adding_buttons)
async def send_welcome(message: types.Message, state: FSMContext):
    await state.update_data(inline_kb_text=message.text)

    data = await state.get_data()
    kb_text = data.get('inline_kb_text')
    message_id = data.get('message_id')
    custom_kb = kb.create_user_keyboard(logic.convert_input_to_buttons(kb_text))
    await bot.copy_message(message.from_id, message.from_id, message_id, reply_markup=custom_kb)

    await message.answer(texts.confirm_message, reply_markup=kb.message_menu_kb)
    await State.confirmation_message.set()




# @dp.message_handler(state=State.confirmation_message)
# async def send_welcome(message: types.Message, state: FSMContext):
#     if message.text == texts.yes:
#         data = await state.get_data()
#         chat_id = data.get('channel_id')
#         message_id = data.get('message_id')
#         await bot.copy_message(chat_id, message.from_id, message_id)
#     elif message.text == texts.no:
#         await message.answer(texts.abort)
#         await message.answer(texts.enter_code)
#         await State.entering_code.set()
#     else:
#         await message.answer(texts.use_kb)
    

