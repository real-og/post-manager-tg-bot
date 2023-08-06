import textwrap
from datetime import datetime, timedelta


admin_welcome = 'Ты администратор. Выбирай, что сделать.'

your_channels = 'Добавленные каналы и группы(проследи чтобы бот имел права администратора)'

abort = 'Отмена'

resend_message = 'Добавьте бота администратором в канал или группу и перешлите сюда любое сообщение из канала или группы'

success = 'Успех'

success_added = 'Успешно добавлено'
success_deleted = 'Успешно удалено'

error_forwarded = 'Ошибка при пересылке. Проверьте сообщение'

delete_channels = 'Нажимай на канал, который хочешь удалить.'

choose_to_create_code = 'Выбирай канал, для которого создается код'

error_bot_rights = 'Проблема с правами бота в канале'

choose_code_type = 'Выбирай тип кода'

type_1 = 'Навсегда'
type_2 = '2 поста в день'

def success_added_code(code, channel_id, day_amount, all_post_number, tg_post_number, name):
    if day_amount == '0':
        day_amount = 'Бесконечность'  
    return textwrap.dedent(f"""
        Код на {day_amount} дней
        Постов: {all_post_number} 
        C cсылкой на Telegram: {tg_post_number}
        Cоздан для канала: {name}
        <code>{code}</code>
    """)
    

error_channel_id = 'что-то не добавился канал'

enter_code = "Привет! Это бот для размещения своих постов в группах и каналах. \
Чтобы добавить канал, в который можно отправить пост, вводи код, который получил от администратора"

error_code = 'Возникла проблема с кодом. Возможно он неверный, либо истекло количество постов по данному коду'

success_code = 'Код принят, вводи сообщение для отправки:'

confirm_message = 'Уверены, что хотите отправить данное сообщение?'

yes = 'Да'
no = 'Нет'

use_kb = 'Используйте клавиатуру'

instruction_for_buttons = 'Добавляйте кнопки используя следующий синтаксис:\n\
текст_кнопки - (дефис) ссылка_для_кнопки\nНапример:\n\n<code>Кнопка 1 - http://example1.com\nКнопка 2 - http://example2.com</code>'

success_posted = 'Отправлено!'

ask_for_day_to_send = 'Выбирайте день для отправки'

choose_time = 'Выбирай время.\nПиши в формате 13:12 То есть час (от 0 до 23) двуеточие и минута (от 0 до 59)\nНапример:\n\n<code>13:12</code>'

success_planned = 'Успешно запланировано.'

channels_btn = 'Каналы'
add_channel_btn = 'Добавить канал'
delete_channel_btn = 'Удалить канал'
create_code_btn = 'Создать код'


instruction_to_get_menu = 'Ты в меню'

error_buttons = 'Какая-то проблема, смотри внимательно формат присылаемого сообщения'

change_message = 'Присылай сообщение для отправки'

error_time = 'Проверь формат времени'

choose_code_days = 'Введите количество суток, где "0" - навсегда'

error_number_expected = 'Ошибка формата ввода'

error_day_amount_too_much = "Значение больше 90"

error_post_amount_too_much = "Значение больше 1000"

choose_post_whole_amount = 'Введите количество постов'

choose_post_tg_amount = 'Введите количество постов ссылками на Telegram'

error_link_violation = 'Ссылка на ресурс телеграм недоступна'

enter_code_btn = 'Ввести код'

def generate_success_code(code):
    datetime_expiration = code['creation_datetime'] + timedelta(days=code['limit_days'])
    if code['limit_days'] == 0:
        formatted_dt = 'Навсегда'
    else:
        formatted_dt = datetime_expiration.strftime("%d.%m.%Y %H:%M")
    return textwrap.dedent(f"""
        Канал активирован до: {formatted_dt}
        Всего постов: {code['limit_count_all'] - code['usage_count']}
        Постов с ссылкой на Telegram: {code['limit_count_tg_link'] - code['tg_link_usage_count']}
    """)

create_post_btn = 'Отправить пост'

type_post = 'Пиши свое сообщение'

enter_code_short = "Вводи код"

error_code_deleted = 'Код недоступен'

def generate_planned_posted(name=None):
    return f'Запланированное сообщение отправлено в канал {name}'