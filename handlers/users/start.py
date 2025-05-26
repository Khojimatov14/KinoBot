import asyncio
from aiogram import F
from zoneinfo import ZoneInfo
from data.config import CHANNELS, ADMINS
from sqlite3 import IntegrityError
from loader import dp, bot, users_db
from aiogram.filters import StateFilter
from states import UserStates, AdminStates
from aiogram.fsm.context import FSMContext
from utils import subscription, send_zip_data
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from keyboards import main_keyboards, channels_keyboard
from aiogram.filters.command import CommandStart, Command


@dp.message(F.content_type == "video")
async def movie_video(message: Message, state: FSMContext):
    video = message.video

    # file_size_bytes = video.file_size
    # file_size_mb = file_size_bytes / (1024 * 1024)  # MB ga o'tkazish
    # file_size_gb = file_size_bytes / (1024 * 1024 * 1024)  # GB ga o'tkazish
    #
    # if file_size_gb >= 1:
    #     print(f"{file_size_gb:.2f} GB")
    # else:
    #     print(f"{file_size_mb:.1f} MB")


    # duration_in_seconds = video.duration
    # hours = duration_in_seconds // 3600
    # minutes = (duration_in_seconds % 3600) // 60
    #
    # print(f"{hours} soat {minutes} daqiqa")
    # print(video.file_name)


@dp.message(Command("bot"))
async def bot_start(message: Message):
    await message.answer(text="Assalomu alekum\n\nAgar sizga Telegram bot yaratish hizmati kerak bo'lsa menga yozing! "
                              "Yoki qo'ng'iroq qiling!\n\nTelegram: @khojimatov14\n+998 90-626-66-44")


@dp.message(Command("senddb"), F.from_user.id.in_(ADMINS))
async def send_zip(message: Message):
    await message.answer(text="DB yuborildi")
    await send_zip_data()


@dp.message(CommandStart())
async def bot_start(message: Message, state: FSMContext):
    await message.answer(text=f"Eng yangi kinolarni tomosha qiling!",
                         reply_markup=main_keyboards(user_id=message.from_user.id))
    await state.set_state(UserStates.main)
    try:
        users_db.add_user(user_id=message.from_user.id,
                          user_name=message.from_user.username,
                          user_first_name=message.from_user.first_name,
                          user_last_name=message.from_user.last_name,
                          user_registration_date=message.date.astimezone(tz=ZoneInfo("Asia/Tashkent")).strftime("%d.%m.%Y | %H:%M:%S"))
    except IntegrityError:
        pass
    # movies_info_db.set_starting_movie_id(1000)



@dp.message(StateFilter(UserStates.main, UserStates.show_movie, UserStates.show_movie_in_search,
                        UserStates.movies, UserStates.select_format, UserStates.select_format_in_search,
                        AdminStates.language))
async def dont_type(message: Message):
    await message.delete()
    rem = await message.answer(text="⚠️ Bu bo'limda habar yuborish taqiqlanadi!")
    await asyncio.sleep(5)
    await rem.delete()


@dp.callback_query(F.data == "back", StateFilter(UserStates.search, UserStates.movies, AdminStates.admin))
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=f"Eng yangi kinolarni tomosha qiling!",
                                 reply_markup=main_keyboards(user_id=call.from_user.id))
    await state.set_state(UserStates.main)


@dp.callback_query(F.data == "check_sub")
async def check_subscription(call: CallbackQuery, state: FSMContext):
    final_status = True
    non_sub_channels = []
    for channel in CHANNELS:
        status = await subscription(user_id=call.from_user.id, channel=channel)
        final_status *= status
        if not status:
            non_sub_channels.append(await bot.get_chat(channel))
    if not final_status:
        try:
            await call.message.edit_text(text="Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling!",
                                         reply_markup=channels_keyboard(channels=non_sub_channels))
        except TelegramBadRequest:
            pass
    else:
        await call.message.edit_text(text=f"Eng yangi kinolarni tomosha qiling!",
                                     reply_markup=main_keyboards(user_id=call.from_user.id))
        await state.set_state(UserStates.main)


@dp.message(Command("bot"))
async def bot_start(message: Message):
    await message.answer(text="Assalomu alekum\n\nAgar sizga Telegram bot yaratish hizmati kerak bo'lsa menga yozing! "
                              "Yoki qo'ng'iroq qiling!\n\nTelegram: @khojimatov14\n+998 90-626-66-44")
