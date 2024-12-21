from aiogram import F
from data import ADMINS
from states import AdminStates
from loader import dp, movies_info_db, movies_db
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards import movies_keyboard, edit_keyboard, admin_main_keyboards, language_keyboard, formats_keyboard


@dp.callback_query(F.from_user.id.in_(ADMINS) & F.data == 'edit', AdminStates.admin)
async def edit_movie(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Qaysi kinoni tahrirlamoqchisiz?", reply_markup=movies_keyboard(page=1, user_id=call.from_user.id))
    await state.set_state(AdminStates.select_edit_movie)
    await state.update_data(page=1)


@dp.callback_query(F.data == "back", AdminStates.select_edit_movie)
async def back_to_admin(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Kerakli bo'limni tanlang!", reply_markup=admin_main_keyboards)
    await state.set_state(AdminStates.admin)


@dp.callback_query(F.data.startswith("page_"), AdminStates.select_edit_movie)
async def edit_movie2(call: CallbackQuery, state: FSMContext):
    page = int(call.data.split("_")[1])
    await call.message.edit_reply_markup(reply_markup=movies_keyboard(page=page, user_id=call.from_user.id))
    await state.update_data(page=page)


@dp.callback_query(F.data.isdigit(), AdminStates.select_edit_movie)
async def edit_movie3(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Kinoning nimasini tahrirlamoqchisiz?", reply_markup=edit_keyboard)
    await state.set_state(AdminStates.how_edit)
    await state.update_data(movie_id=int(call.data))


@dp.callback_query(F.data == "back", AdminStates.how_edit)
async def back_to_admin(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.edit_text(text="Qaysi kinoni tahrirlamoqchisiz?", reply_markup=movies_keyboard(page=data["page"], user_id=call.from_user.id))
    await state.set_state(AdminStates.select_edit_movie)

# Name
@dp.callback_query(F.data == "name", AdminStates.how_edit)
async def edit_name1(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Kinoning nomini kiriting!")
    await state.set_state(AdminStates.edit_name)


@dp.message(AdminStates.edit_name)
async def edit_name2(message: Message, state: FSMContext):
    await message.answer(text="Kinoning nomi o'zgartirildi!", reply_markup=edit_keyboard)
    await state.set_state(AdminStates.how_edit)
    data = await state.get_data()
    movies_info_db.update_movie_info(movie_id=data["movie_id"], movie_name=message.text)


# Country
@dp.callback_query(F.data == "country", AdminStates.how_edit)
async def edit_country1(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Davlatini kiriting!")
    await state.set_state(AdminStates.edit_country)


@dp.message(AdminStates.edit_country)
async def edit_country2(message: Message, state: FSMContext):
    await message.answer(text="Kinoning davlati o'zgartirildi!", reply_markup=edit_keyboard)
    await state.set_state(AdminStates.how_edit)
    data = await state.get_data()
    movies_info_db.update_movie_info(movie_id=data["movie_id"], movie_country=message.text)


# Year
@dp.callback_query(F.data == "year", AdminStates.how_edit)
async def edit_year1(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Yilni kiriting!")
    await state.set_state(AdminStates.edit_year)


@dp.message(AdminStates.edit_year)
async def edit_year2(message: Message, state: FSMContext):
    await message.answer(text="Kinoning yili o'zgartirildi!", reply_markup=edit_keyboard)
    await state.set_state(AdminStates.how_edit)
    data = await state.get_data()
    movies_info_db.update_movie_info(movie_id=data["movie_id"], movie_year=message.text)


# Language
@dp.callback_query(F.data == "language", AdminStates.how_edit)
async def edit_language1(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Tilini tanlang.", reply_markup=language_keyboard)
    await state.set_state(AdminStates.edit_language)


@dp.callback_query(F.data.startswith("lan_"), AdminStates.edit_language)
async def edit_language2(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Kinoning tili o'zgartirildi!", reply_markup=edit_keyboard)
    await state.set_state(AdminStates.how_edit)

    language = call.data.split("_")[1]
    language = "O'zbekcha" if language == "uzb" else "Ruscha"
    data = await state.get_data()
    movies_info_db.update_movie_info(movie_id=data["movie_id"], movie_language=language)


# Time
@dp.callback_query(F.data == "time", AdminStates.how_edit)
async def edit_time1(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Vaqtini kiriting!")
    await state.set_state(AdminStates.edit_time)


@dp.message(AdminStates.edit_time)
async def edit_time2(message: Message, state: FSMContext):
    await message.answer(text="Kinoning vaqti o'zgartirildi!", reply_markup=edit_keyboard)
    await state.set_state(AdminStates.how_edit)
    data = await state.get_data()
    movies_info_db.update_movie_info(movie_id=data["movie_id"], movie_time=message.text)


# Video
@dp.callback_query(F.data == "new_video", AdminStates.how_edit)
async def edit_time1(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Video formatini tanlang!", reply_markup=formats_keyboard)
    await state.set_state(AdminStates.add_new_video)


@dp.callback_query(F.data.startswith("f_"), AdminStates.add_new_video)
async def edit_time2(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Videoni yuboring!\n\nIltimos video to'liq yuklanmagunicha hech narsa qilmang!")
    await state.set_state(AdminStates.get_new_video)
    await state.update_data(format=call.data.split("_")[1])


@dp.message(F.content_type == "video", AdminStates.get_new_video)
async def movie_video(message: Message, state: FSMContext):
    await message.answer(text=f"Video muvaffaqiyatli yuklandi!", reply_markup=edit_keyboard)
    await state.set_state(AdminStates.how_edit)
    data = await state.get_data()
    movies_db.add_movie(movie_id=data["movie_id"], movie_format=data["format"], movie_file_id=message.video.file_id)
