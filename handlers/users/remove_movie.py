from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from data import ADMINS
from keyboards import movies_keyboard, admin_main_keyboards
from loader import dp, movies_info_db, movies_db
from states import AdminStates


@dp.callback_query(F.from_user.id.in_(ADMINS) & F.data == 'remove', AdminStates.admin)
async def add_movie(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Qaysi kinoni o'chirmoqchisiz?", reply_markup=movies_keyboard(page=1, user_id=call.from_user.id))
    await state.set_state(AdminStates.remove_movie)
    await state.update_data(page=1)


@dp.callback_query(F.data == "back", AdminStates.remove_movie)
async def back_to_admin(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Kerakli bo'limni tanlang!", reply_markup=admin_main_keyboards)
    await state.set_state(AdminStates.admin)


@dp.callback_query(F.data.startswith("page_"), AdminStates.remove_movie)
async def edit_movie2(call: CallbackQuery, state: FSMContext):
    page = int(call.data.split("_")[1])
    await call.message.edit_reply_markup(reply_markup=movies_keyboard(page=page, user_id=call.from_user.id))
    await state.update_data(page=page)


@dp.callback_query(F.data.isdigit(), AdminStates.remove_movie)
async def edit_movie3(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    movies_info_db.delete_movie_by_id(movie_id=int(call.data))
    movies_db.delete_movies_by_id(movie_id=int(call.data))
    await call.message.edit_text(text=f"{call.data} kodli kino o'chirildi", reply_markup=movies_keyboard(page=data["page"], user_id=call.from_user.id))
