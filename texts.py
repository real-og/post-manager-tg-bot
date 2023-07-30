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

def success_added_code(code, channel, type):
    return f"Код типа {type} создан для канала {channel}\n\n<code>{code}</code>"

error_channel_id = 'что-то не добавился канал'

enter_code = "Привет! Это бот для размещения своих постов в группах и каналах. \
Чтобы начать создавать пост, вводи код, который получил от администратора"

error_code = 'Возникла проблема с кодом. Возможно он неверный, либо истекло количество постов по данному коду'

success_code = 'Код принят, вводи сообщение для отправки:'

confirm_message = 'Уверены, что хотите отправить данное сообщение?'

yes = 'Да'
no = 'Нет'

use_kb = 'Используйте клавиатуру'

instruction_for_buttons = 'Добавляйте кнопки используя следующий синтаксис:\n\
текст_кнопки - (дефис) ссылка_для_кнопки\nНапример:\n\n<code>Кнопка 1 - http://example1.com\nКнопка 2 - http://example2.com</code>'

success_posted = 'Отправлено! Чтобы продолжить, вводи код.'

ask_for_day_to_send = 'Выбирайте день для отправки'

choose_time = 'Выбирай время.\nПиши в формате 13:12 То есть час (от 0 до 23) двуеточие и минута (от 0 до 59)\nНапример:\n\n<code>13:12</code>'

success_planned = 'Успешно запланировано. Чтобы продолжить, вводи код'

channels_btn = 'Каналы'
add_channel_btn = 'Добавить канал'
delete_channel_btn = 'Удалить канал'
create_code_btn = 'Создать код'


instruction_to_get_menu = 'Ты в меню'

error_buttons = 'Какая-то проблема, смотри внимательно формат присылаемого сообщения'

change_message = 'Присылай сообщение для отправки'

error_time = 'Проверь формат времени'
