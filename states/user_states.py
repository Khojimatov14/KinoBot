from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    check_sub = State()
    show_movie_in_search = State()
    select_format_in_search = State()
    select_format = State()
    show_movie = State()
    movies = State()
    search = State()
    main = State()