from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    remove_movie = State()
    send_message = State()
    get_new_video = State()
    add_new_video = State()
    edit_time = State()
    edit_language = State()
    edit_year = State()
    edit_country = State()
    edit_name = State()
    how_edit = State()
    select_edit_movie = State()
    movie = State()
    format = State()
    caption = State()
    time = State()
    language = State()
    year = State()
    country = State()
    name = State()
    admin = State()