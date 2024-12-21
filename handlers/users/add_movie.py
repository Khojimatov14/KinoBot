from aiogram import F
from data import ADMINS
from states import AdminStates
from aiogram.fsm.context import FSMContext
from loader import dp, movies_info_db, movies_db
from aiogram.types import CallbackQuery, Message
from keyboards import formats_keyboard, admin_main_keyboards, language_keyboard


@dp.callback_query(F.from_user.id.in_(ADMINS) & F.data == 'add', AdminStates.admin)
async def add_movie(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Kinoning nomini kiriting!")
    await state.set_state(AdminStates.name)


@dp.message(F.from_user.id.in_(ADMINS), AdminStates.name)
async def movie_name(message: Message, state: FSMContext):
    await message.answer(text="Davlatini kiriting!")
    await state.update_data(name=message.text)
    await state.set_state(AdminStates.country)


@dp.message(F.from_user.id.in_(ADMINS), AdminStates.country)
async def movie_country(message: Message, state: FSMContext):
    await message.answer(text="Yilni kiriting!")
    await state.update_data(country=message.text)
    await state.set_state(AdminStates.year)


@dp.message(F.from_user.id.in_(ADMINS), AdminStates.year)
async def movie_year(message: Message, state: FSMContext):
    await message.answer(text="Vaqtini kiriting!")
    await state.update_data(year=message.text)
    await state.set_state(AdminStates.time)


@dp.message(F.from_user.id.in_(ADMINS), AdminStates.time)
async def movie_time(message: Message, state: FSMContext):
    await message.answer(text="Tilini tanlang.", reply_markup=language_keyboard)
    await state.update_data(time=message.text)
    await state.set_state(AdminStates.language)


@dp.callback_query(F.from_user.id.in_(ADMINS) & F.data.startswith("lan_"), AdminStates.language)
async def movie_language(call: CallbackQuery, state: FSMContext):
    language = call.data.split("_")[1]
    language = "O'zbekcha" if language == "uzb" else "Ruscha"
    await call.message.edit_text(text="Kino formatini tanlang!", reply_markup=formats_keyboard)
    await state.update_data(language=language)
    await state.set_state(AdminStates.format)


@dp.callback_query(F.from_user.id.in_(ADMINS) & F.data.startswith("f_"), AdminStates.format)
async def movie_format(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Kinoni yuboring!\n\nIltimos kino to'liq yuklanmagunicha hech narsa qilmang!")
    await state.update_data(format=call.data.split("_")[1])
    await state.set_state(AdminStates.movie)


@dp.message(F.from_user.id.in_(ADMINS) & F.content_type == "video", AdminStates.movie)
async def movie_video(message: Message, state: FSMContext):
    data = await state.get_data()
    movies_info_db.add_movie(movie_name=data["name"], movie_country=data["country"], movie_year=data["year"],
                             movie_language=data["language"], movie_time=data["time"])
    last_movie = movies_info_db.get_last_movie_info()
    movies_db.add_movie(movie_id=last_movie[0], movie_format=data["format"], movie_file_id=message.video.file_id)

    await message.answer(text=f"✅ Kino muvaffaqiyatli yuklandi!\n\n🔢 Kino kod: {last_movie[0]}", reply_markup=admin_main_keyboards)
    await state.set_state(AdminStates.admin)
