from aiogram.dispatcher.filters.state import StatesGroup, State


class State(StatesGroup):
    waiting_message_from_channels = State()
