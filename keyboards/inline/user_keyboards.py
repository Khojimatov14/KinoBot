from math import ceil
from data import ADMINS
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_keyboards(user_id):
    keyboards = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔍 Kino qidirish", callback_data="search"),
            ],
            [
                # InlineKeyboardButton(text="⭐️ Saqlangan kinolar", callback_data="saved"),
                InlineKeyboardButton(text="🎬 Barcha kinolar", callback_data="movies"),
            ],
        ]
    )

    if user_id in ADMINS:
        keyboards.inline_keyboard.append(
            [
                InlineKeyboardButton(text="👨‍💻 Admin", callback_data="admin")
            ]
        )

    return keyboards


def movies_keyboard(page, user_id=0):
    movie_code = False
    if user_id in ADMINS:
        movie_code = True

    from loader import movies_info_db
    movies = movies_info_db.get_all_movies_info()

    keyboards = InlineKeyboardMarkup(inline_keyboard=[])

    items_per_page = 4
    pages = ceil(len(movies) / items_per_page)
    start = (page - 1) * items_per_page
    end = start + items_per_page
    current_page_movies = movies[start:end]

    if movie_code:
        for movie in current_page_movies:
            keyboards.inline_keyboard.append([InlineKeyboardButton(text=f"{movie[1]} | {movie[0]}", callback_data=str(movie[0]))])
    else:
        for movie in current_page_movies:
            keyboards.inline_keyboard.append([InlineKeyboardButton(text=movie[1], callback_data=str(movie[0]))])

    if pages > 1:
        pagination_buttons = []
        if page > 1:
            back_data = f"page_{page-1}"
            button_text = "◀️"
        else:
            back_data = "none"
            button_text = "#️⃣"
        pagination_buttons.append(InlineKeyboardButton(text=button_text, callback_data=back_data))
        pagination_buttons.append(InlineKeyboardButton(text=f"{page}/{pages}", callback_data="none"))
        if page < pages:
            next_data = f"page_{page+1}"
            button_text = "▶️"
        else:
            next_data = "none"
            button_text = "#️⃣"
        pagination_buttons.append(InlineKeyboardButton(text=button_text, callback_data=next_data))
        keyboards.inline_keyboard.append(pagination_buttons)

    keyboards.inline_keyboard.append([InlineKeyboardButton(text="⬅️ Ortga", callback_data="back")])

    return keyboards


back_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️ Ortga", callback_data="back"),
            ]
        ]
    )


def movie_formats_keyboard(movies):
    video_formats = [item[1] for item in movies]
    video_formats.sort(key=lambda x: int(x.replace('p', '').replace('k', '000')))

    keyboards = InlineKeyboardMarkup(inline_keyboard=[])
    for video_format in video_formats:
        keyboards.inline_keyboard.append([InlineKeyboardButton(text=video_format, callback_data=video_format)])
    return keyboards


def channels_keyboard(channels):
    keyboards = InlineKeyboardMarkup(inline_keyboard=[])
    for channel in channels:
        keyboards.inline_keyboard.append([InlineKeyboardButton(text=channel.title, url=channel.invite_link)])
    keyboards.inline_keyboard.append([InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")])
    return keyboards

