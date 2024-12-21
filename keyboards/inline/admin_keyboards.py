from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


admin_main_keyboards = InlineKeyboardMarkup(
    inline_keyboard=[
        [
                InlineKeyboardButton(text="➕ Kino qo'shish", callback_data="add"),
                InlineKeyboardButton(text="➖ Kino o'chirish", callback_data="remove"),
        ],
        [
                InlineKeyboardButton(text="📝 Kinoni tahrirlash", callback_data="edit"),
        ],
        [
            InlineKeyboardButton(text="📨 Obunachilarga habar yuborish", callback_data="send"),
        ],
        [
            InlineKeyboardButton(text="Auto get DB", callback_data="get_db"),
        ],
        [
            InlineKeyboardButton(text="⬅️ Ortga", callback_data="back"),
        ]
    ]
)


edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Video qo'shish", callback_data="new_video"),
            InlineKeyboardButton(text="✏️ Nomi", callback_data="name"),
        ],
        [
            InlineKeyboardButton(text="🌐 Davlati", callback_data="country"),
            InlineKeyboardButton(text="📆 Yili", callback_data="year"),

        ],
        [
            InlineKeyboardButton(text="🔊 Tili", callback_data="language"),
            InlineKeyboardButton(text="⏳ Vaqti", callback_data="time"),

        ],
        [
            InlineKeyboardButton(text="⬅️ Ortga", callback_data="back"),
        ]
    ]
)


formats_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="480p", callback_data="f_480p"),
        ],
        [
            InlineKeyboardButton(text="720p", callback_data="f_720p"),
        ],
        [
            InlineKeyboardButton(text="1080p", callback_data="f_1080p"),
        ],
        [
            InlineKeyboardButton(text="4k", callback_data="f_4k"),
        ],
        [
            InlineKeyboardButton(text="8k", callback_data="f_8k"),
        ],
    ]
)


language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="O'zbekcha", callback_data="lan_uzb"),
        ],
        [
            InlineKeyboardButton(text="Ruscha", callback_data="lan_rus"),
        ]
    ]
)
