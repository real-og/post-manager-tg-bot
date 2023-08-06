from loader import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
import texts
from states import *
import logic
import keyboards as kb
import db
from handlers.users.commands import send_welcome_user

@dp.message_handler(state=State.user_code_view)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.text == texts.abort:
        await send_welcome_user(message, state)
        return
    elif message.text == texts.create_post_btn:
        await message.answer(texts.type_post, reply_markup=kb.abort_kb)
        await State.typing_message.set()
    else:
        await message.answer(texts.use_kb)


@dp.message_handler(state=State.typing_message,
                    content_types=types.ContentType.ANY)
async def send_welcome(message: types.Message, state: FSMContext):
    if message.text == texts.abort:
        await send_welcome_user(message, state)
        return
    message_to_send = await message.send_copy(message.from_id)
    message_id = message_to_send.message_id
    await state.update_data(message_id=message_id)
    await message.answer(texts.confirm_message, reply_markup=kb.message_menu_kb)
    await State.confirmation_message.set()

@dp.message_handler(state=State.changing_message,
                    content_types=types.ContentType.ANY)
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
    data = await state.get_data()
    kb_text = data.get('inline_kb_text')
    custom_kb = kb.create_user_keyboard(logic.convert_input_to_buttons(kb_text))

    message_to_send = await message.send_copy(message.from_id, reply_markup=custom_kb)
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
        code = data.get('code')
        custom_kb = kb.create_user_keyboard(logic.convert_input_to_buttons(kb_text))

        if chat_id == '0' or chat_id == 0:
            sended = 0
            channels = db.get_channels()
            for ch in channels:
                if ch.get('channel_id') == '0' or ch.get('channel_id') == 0:
                    continue
                try:
                    await bot.copy_message(ch.get('channel_id'), callback.from_user.id, message_id, reply_markup=custom_kb)
                    sended += 1
                except:
                    await bot.send_message(callback.from_user.id, texts.error_bot_rights)
            if sended > 0:
                await callback.message.answer(texts.success_posted)
                if kb_text is not None and 'https://t.me/' in kb_text:
                    db.implement_usage_count_for_code(code, True)
                else:
                    db.implement_usage_count_for_code(code, False)

            user_codes = data.get('user_codes')
            await state.update_data(inline_kb_text=None)
            await state.update_data(channel_id=None)
            if user_codes is None:
                await state.update_data(user_codes=[])
            await callback.message.answer(texts.enter_code, reply_markup=kb.create_user_menu(user_codes))
            await State.user_menu.set()          
            return
        try:
            await bot.copy_message(chat_id, callback.from_user.id, message_id, reply_markup=custom_kb)
        except Exception as e:
            await callback.message.answer(texts.error_bot_rights)
            return

        if kb_text is not None and 'https://t.me/' in kb_text:
            db.implement_usage_count_for_code(code, True)
        else:
            db.implement_usage_count_for_code(code, False)
        await callback.message.answer(texts.success_posted)
        user_codes = data.get('user_codes')
        await state.update_data(inline_kb_text=None)
        await state.update_data(channel_id=None)
        if user_codes is None:
            await state.update_data(user_codes=[])
        await callback.message.answer(texts.enter_code, reply_markup=kb.create_user_menu(user_codes))
        await State.user_menu.set()

    elif callback.data == 'buttons':
        await callback.message.answer(texts.instruction_for_buttons, reply_markup=kb.abort_kb)
        await State.adding_buttons.set()

    elif callback.data == 'schedule':
        await callback.message.answer(texts.ask_for_day_to_send, reply_markup=kb.choose_day_kb)
        await State.choosing_day.set()

    elif callback.data == 'change':
        await callback.message.answer(texts.change_message)
        await State.changing_message.set()

    elif callback.data == 'abort':
        data = await state.get_data()
        user_codes = data.get('user_codes')
        await state.update_data(inline_kb_text=None)
        await state.update_data(channel_id=None)
        if user_codes is None:
            await state.update_data(user_codes=[])
        await callback.message.answer(texts.enter_code, reply_markup=kb.create_user_menu(user_codes))
        await State.user_menu.set()
        


@dp.message_handler(state=State.adding_buttons)
async def send_welcome(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == texts.abort:
        message_id = data.get('message_id')
        kb_text = data.get('inline_kb_text')
        custom_kb = kb.create_user_keyboard(logic.convert_input_to_buttons(kb_text))
        await bot.copy_message(message.from_id, message.from_id, message_id, reply_markup=custom_kb)
        await message.answer(texts.confirm_message, reply_markup=kb.message_menu_kb)
        await State.confirmation_message.set()
        return
    
    code = data.get('code')
    if not logic.check_is_link_allowed(code) and 'https://t.me/' in message.text:
        await message.answer(texts.error_link_violation, reply_markup=kb.abort_kb)
        return
    await state.update_data(inline_kb_text=message.text)

    data = await state.get_data()
    kb_text = data.get('inline_kb_text')
    message_id = data.get('message_id')
    try:
        custom_kb = kb.create_user_keyboard(logic.convert_input_to_buttons(kb_text))
    except:
        await message.answer(texts.error_buttons, reply_markup=kb.abort_kb)
        return
    try:
        await bot.copy_message(message.from_id, message.from_id, message_id, reply_markup=custom_kb)
    except:
        await message.answer(texts.error_buttons, reply_markup=kb.abort_kb)
        return

    await message.answer(texts.confirm_message, reply_markup=kb.message_menu_kb)
    await State.confirmation_message.set()

