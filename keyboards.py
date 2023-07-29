from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

import texts

def generate_channel_kb(channels):
    kb = InlineKeyboardMarkup(row_width=1)
    for channel in channels:
        kb.add(InlineKeyboardButton(channel['name'], callback_data=channel['channel_id']))
    return kb

abort_kb = ReplyKeyboardMarkup([[texts.abort]])

code_types_kb = InlineKeyboardMarkup(row_width=1)
code_types_kb.add(InlineKeyboardButton(texts.type_1, callback_data='0'))
code_types_kb.add(InlineKeyboardButton(texts.type_2, callback_data='1'))

yes_no_kb = ReplyKeyboardMarkup([[texts.yes, texts.no]], one_time_keyboard=True)


message_menu_kb = InlineKeyboardMarkup(row_width=1)
message_menu_kb.add(InlineKeyboardButton('Добавить URL-кнопки', callback_data='buttons'))
message_menu_kb.add(InlineKeyboardButton('Отправить сейчас', callback_data='finish'))
message_menu_kb.add(InlineKeyboardButton('Запланировать отправку', callback_data='schedule'))


choose_day_kb = InlineKeyboardMarkup(row_width=1)
choose_day_kb.add(InlineKeyboardButton('Сегодня', callback_data='today'))
choose_day_kb.add(InlineKeyboardButton('Завтра', callback_data='tomorrow'))
choose_day_kb.add(InlineKeyboardButton('Послезавтра', callback_data='after_tomorrow'))

def create_user_keyboard(title_url_pairs):
    kb = InlineKeyboardMarkup(row_width=1)
    for pair in title_url_pairs:
        kb.add(InlineKeyboardButton(pair[0], pair[1]))
    return kb

admin_menu_kb = ReplyKeyboardMarkup([[texts.channels_btn, texts.add_channel_btn, texts.delete_channel_btn],
                                      [texts.create_code_btn]], resize_keyboard=True, one_time_keyboard=True)
