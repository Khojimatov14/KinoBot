import asyncio

from aiogram import F
from aiogram.filters import Command

from loader import dp
from data import ADMINS
from aiogram.types import CallbackQuery
from states import UserStates, AdminStates
from keyboards import admin_main_keyboards
from aiogram.fsm.context import FSMContext

from utils import send_zip_data


@dp.callback_query(F.from_user.id.in_(ADMINS) & F.data == 'admin', UserStates.main)
async def admin_all_commands(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Kerakli bo'limni tanlang!", reply_markup=admin_main_keyboards)
    await state.set_state(AdminStates.admin)


@dp.callback_query(F.from_user.id.in_(ADMINS) & F.data == 'get_db', AdminStates.admin)
async def add_movie(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    if data.get("auto_db") is None:
        await state.update_data(auto_db=True)
        await call.message.edit_text(text="Malumotlar bazasini avtomatik yuborish boshlandi!", reply_markup=admin_main_keyboards)
        while True:
            await send_zip_data()
            await asyncio.sleep(43200)
    else:
        await call.message.edit_text(text="Malumotlar bazasini avtomatik yuborish avval boshlangan!", reply_markup=admin_main_keyboards)
