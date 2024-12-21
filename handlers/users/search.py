import asyncio
from aiogram import F
from states import UserStates
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from loader import dp, movies_info_db, movies_db, bot
from keyboards import back_keyboard, movie_formats_keyboard


@dp.callback_query(F.data == "search", UserStates.main)
async def search_movie(call: CallbackQuery, state: FSMContext):
    msg = await call.message.edit_text(text="Kino ko'dini yoki nomini kiriting!", reply_markup=back_keyboard)
    await state.set_state(UserStates.search)
    await state.update_data(message_id=msg.message_id)


@dp.message(UserStates.search)
async def search_movie2(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        if message.text.isdigit():
            movie_video = movies_db.select_movie_by_id(movie_id=int(message.text))
            movie_info = movies_info_db.select_movie_info(movie_id=int(message.text))

            if movie_video and movie_info:
                if len(movie_video) == 1:
                    await message.answer_video(video=movie_video[0][2],
                                               caption=f"<b>🎬 Nomi:</b> {movie_info[1]}\n\n<b>📺 Sifati:</b> {movie_video[0][1]}\n"
                                                       f"<b>🌍 Davlati:</b> {movie_info[2]}\n<b>📆 Yili:</b> {movie_info[3]}\n"
                                                       f"<b>🔊 Tili:</b> {movie_info[4]}\n<b>⏳ Davomiyligi:</b> {movie_info[5]}",
                                               reply_markup=back_keyboard)
                    await state.set_state(UserStates.show_movie_in_search)
                    await bot.edit_message_text(text="Kino ko'dini yoki nomini kiriting!",
                                                chat_id=message.chat.id,
                                                message_id=data["message_id"])

                elif len(movie_video) > 1:
                    await message.answer(text="Kerakli formatni tanlang!",
                                         reply_markup=movie_formats_keyboard(movies=movie_video))
                    await state.set_state(UserStates.select_format_in_search)
                    await bot.edit_message_text(text="Kino ko'dini yoki nomini kiriting!",
                                                chat_id=message.chat.id,
                                                message_id=data["message_id"])
                    await state.update_data(movie_id=int(message.text))

            else:
                rem1 = await message.answer(text="Bunday ko'dli kino mavjud emas!")
                await asyncio.sleep(5)
                await rem1.delete()
                await message.delete()

        elif message.text.isalpha():
            rem = await message.answer(text="☹️ Kechirasiz kinoni nomidan qidirish funksiyasi vaqtinchalik o'chirib "
                                            "qo'yilgan.\n\nIltimos kino ko'dini kiriting!")
            await asyncio.sleep(5)
            await rem.delete()

        else:
            await message.delete()
            rem = await message.answer(text="Iltimos kino ko'dini yoki nomini kiriting!")
            await asyncio.sleep(5)
            await rem.delete()

    except AttributeError:
        await message.delete()
        rem = await message.answer(text="Iltimos kino ko'dini yoki nomini kiriting!")
        await asyncio.sleep(5)
        await rem.delete()


@dp.callback_query(F.data == "back", UserStates.show_movie_in_search)
async def movies3(call: CallbackQuery, state: FSMContext):
    msg = await call.message.answer(text="Kino ko'dini yoki nomini kiriting!", reply_markup=back_keyboard)
    await state.set_state(UserStates.search)
    await call.message.delete_reply_markup()
    await state.update_data(message_id=msg.message_id)


@dp.callback_query(F.data.in_({'480p', '720p', '1080p', '4k', '8k'}), UserStates.select_format_in_search)
async def movies4(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    movie_video = movies_db.select_movie_by_format(movie_id=data["movie_id"], movie_format=call.data)
    movie_info = movies_info_db.select_movie_info(movie_id=data["movie_id"])

    if movie_video and movie_info:
        await call.message.answer_video(video=movie_video[2],
                                        caption=f"<b>🎬 Nomi:</b> {movie_info[1]}\n\n<b>📺 Sifati:</b> {call.data}\n"
                                                f"<b>🌍 Davlati:</b> {movie_info[2]}\n<b>📆 Yili:</b> {movie_info[3]}\n"
                                                f"<b>🔊 Tili:</b> {movie_info[4]}\n<b>⏳ Davomiyligi:</b> {movie_info[5]}",
                                        reply_markup=back_keyboard)
        await state.set_state(UserStates.show_movie_in_search)
        await call.message.delete()