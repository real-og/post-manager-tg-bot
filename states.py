from aiogram.dispatcher.filters.state import StatesGroup, State


class State(StatesGroup):
    waiting_message_from_channels = State()
    deleting_channel = State()
    choosing_to_create_code = State()
    choosing_type_of_code = State()
    entering_code = State()
    typing_message = State()
    confirmation_message = State()