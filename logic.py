import random
import string
import db
import datetime
import texts

def generate_random_code(length):
    code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))
    return code

def check_access_code(code):
    result = db.get_code(code)

    if result is None:
        return None

    # limit_tg_count = result['limit_count_tg_link'] 
    limit_count = result['limit_count_all'] 
    usage_count = result['usage_count'] 
    # usage_tg_count = result['tg_link_usage_count']
    creation_datetime = result['creation_datetime']
    limit_days = result['limit_days']
    

    if limit_count == 0:
        return result['channel_id']
    
    if datetime.datetime.now() - creation_datetime > datetime.timedelta(days=limit_days):
        return None

    if usage_count >= limit_count:
        return None
    
    return result['channel_id']

    

def convert_input_to_buttons(text):
    if text is None:
        return []
    buttons = text.split('\n')
    title_url_pairs = [pair.split(' - ') for pair in buttons]
    return title_url_pairs

async def send_message_time(bot, chat_id, message_id, custom_kb, from_id):
    if chat_id == '0' or chat_id == 0:
        channels = db.get_channels()
        for ch in channels:
            try:
                await bot.copy_message(ch.get('channel_id'), from_id, message_id, reply_markup=custom_kb)
                await bot.send_message(from_id, texts.success_posted + ch.get('name'))
            except:
                await bot.send_message(from_id, texts.error_bot_rights)
        return
    await bot.copy_message(chat_id, from_id, message_id, reply_markup=custom_kb)
    await bot.send_message(from_id, texts.success_posted)

def check_is_link_allowed(code):
    result = db.get_code(code)
    if result is None:
        return None
    usage_tg_count = result['tg_link_usage_count']
    limit_tg_count = result['limit_count_tg_link']
    if usage_tg_count >= limit_tg_count:
        return False
    return True
