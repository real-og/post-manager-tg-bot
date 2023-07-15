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
