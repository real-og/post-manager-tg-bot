from aiogram.dispatcher.filters.state import StatesGroup, State


class State(StatesGroup):
    waiting_message_from_channels = State()
    deleting_channel = State()
    choosing_to_create_code = State()
    choosing_type_of_code = State()
    entering_code = State()
    typing_message = State()
    confirmation_message = State()
    adding_buttons = State()
    choosing_day = State()
    choosing_time = State()
    admin_menu = State()
    choosing_days_of_code = State()
    choosing_all_post_number = State()
    choosing_tg_post_number = State()
    user_menu = State()
    user_code_view = State()
    changing_message = State()