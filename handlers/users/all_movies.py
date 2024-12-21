from aiogram import F
from states import UserStates
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from loader import dp, movies_info_db, movies_db
from keyboards import movies_keyboard, back_keyboard, movie_formats_keyboard


@dp.callback_query(F.data == "movies", UserStates.main)
async def movies1(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="🎬 Barcha kinolar", reply_markup=movies_keyboard(page=1))
    await state.set_state(UserStates.movies)
    await state.update_data(page=1)


@dp.callback_query(F.data.startswith("page_"), UserStates.movies)
async def movies2(call: CallbackQuery, state: FSMContext):
    page = int(call.data.split("_")[1])
    await call.message.edit_reply_markup(reply_markup=movies_keyboard(page=page))
    await state.update_data(page=page)


@dp.callback_query(F.data.isdigit(), UserStates.movies)
async def movies3(call: CallbackQuery, state: FSMContext):
    movie_video = movies_db.select_movie_by_id(movie_id=int(call.data))
    movie_info = movies_info_db.select_movie_info(movie_id=int(call.data))

    if len(movie_video) == 1:
        if movie_video and movie_info:
            await call.message.answer_video(video=movie_video[0][2],
                                            caption=f"<b>🎬 Nomi:</b> {movie_info[1]}\n\n<b>📺 Sifati:</b> {movie_video[0][1]}\n"
                                                    f"<b>🌍 Davlati:</b> {movie_info[2]}\n<b>📆 Yili:</b> {movie_info[3]}\n"
                                                    f"<b>🔊 Tili:</b> {movie_info[4]}\n<b>⏳ Davomiyligi:</b> {movie_info[5]}",
                                            reply_markup=back_keyboard)
            await state.set_state(UserStates.show_movie)
            await call.message.delete()
    elif len(movie_video) > 1:
        await call.message.edit_text(text="Kerakli formatni tanlang!", reply_markup=movie_formats_keyboard(movies=movie_video))
        await state.set_state(UserStates.select_format)
        await state.update_data(movie_id=int(call.data))


@dp.callback_query(F.data == "back", UserStates.show_movie)
async def movies4(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.message.answer(text="🎬 Barcha kinolar", reply_markup=movies_keyboard(page=data["page"]))
    await state.set_state(UserStates.movies)
    await call.message.delete_reply_markup()


@dp.callback_query(F.data.in_({'480p', '720p', '1080p', '4k', '8k'}), UserStates.select_format)
async def movies5(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    movie_video = movies_db.select_movie_by_format(movie_id=data["movie_id"], movie_format=call.data)
    movie_info = movies_info_db.select_movie_info(movie_id=data["movie_id"])

    if movie_video and movie_info:
        await call.message.answer_video(video=movie_video[2],
                                        caption=f"<b>🎬 Nomi:</b> {movie_info[1]}\n\n<b>📺 Sifati:</b> {call.data}\n"
                                                f"<b>🌍 Davlati:</b> {movie_info[2]}\n<b>📆 Yili:</b> {movie_info[3]}\n"
                                                f"<b>🔊 Tili:</b> {movie_info[4]}\n<b>⏳ Davomiyligi:</b> {movie_info[5]}",
                                        reply_markup=back_keyboard)
        await state.set_state(UserStates.show_movie)
        await call.message.delete()
