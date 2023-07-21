import random
import string
import db
import datetime

def generate_random_code(length):
    code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))
    return code

def check_access_code(code):
    result = db.get_code(code)

    if result is None:
        return None

    limit_count = result['limit_count'] 
    usage_count = result['usage_count'] 
    last_reset = result['last_reset'] 

    if limit_count == 0:
        return result['channel_id']
    
    if datetime.datetime.now() - last_reset > datetime.timedelta(hours=24):
        db.reset_usage_count_for_code(code)
        usage_count = 0

    elif usage_count < limit_count:
        return result['channel_id']
    else:
        return None
    

def convert_input_to_buttons(text):
    if text is None:
        return []
    buttons = text.split('\n')
    title_url_pairs = [pair.split(' - ') for pair in buttons]
    return title_url_pairs