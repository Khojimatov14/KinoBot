import asyncio
from aiogram import F
from aiogram.exceptions import TelegramForbiddenError

from loader import dp, users_db, bot
from data import ADMINS
from states import AdminStates, UserStates
from keyboards import main_keyboards
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext


@dp.callback_query(F.from_user.id.in_(ADMINS) & F.data == 'send', AdminStates.admin)
async def edit_movie(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="Habarni kiriting!\n\nSiz Photo, Video va Text ko'rinishidagi habarlarni "
                                      "yuborishingiz mumkun!")
    await state.set_state(AdminStates.send_message)


# Text
@dp.message(F.from_user.id.in_(ADMINS) & F.content_type == "text", AdminStates.send_message)
async def edit_movie(message: Message, state: FSMContext):
    users = users_db.select_all_users()
    real_users = 0
    blocked_users = 0
    for user in users:
        try:
            await bot.send_message(chat_id=user[0], text=message.text)
            await asyncio.sleep(0.3)
            real_users += 1
        except TelegramForbiddenError:
            blocked_users += 1
    await message.answer(text=f"Habar <b>{real_users}</b> ta obunachiga yuborildi\n\n<b>{blocked_users}</b> ta "
                              f"obunachi botni bloklagan\n\nJami obunachilar: {real_users + blocked_users} ta")
    await message.answer(text=f"Eng yangi kinolarni tomosha qiling!",
                         reply_markup=main_keyboards(user_id=message.from_user.id))
    await state.set_state(UserStates.main)


# Photo
@dp.message(F.from_user.id.in_(ADMINS) & F.content_type == "photo", AdminStates.send_message)
async def edit_movie(message: Message, state: FSMContext):
    users = users_db.select_all_users()
    real_users = 0
    blocked_users = 0
    for user in users:
        try:
            await bot.send_photo(chat_id=user[0], photo=message.photo[-1].file_id, caption=message.caption)
            await asyncio.sleep(0.3)
            real_users += 1
        except TelegramForbiddenError:
            blocked_users += 1
    await message.answer(text=f"Habar <b>{real_users}</b> ta obunachiga yuborildi\n\n<b>{blocked_users}</b> ta "
                              f"obunachi botni bloklagan\n\nJami obunachilar: {real_users + blocked_users} ta")
    await message.answer(text=f"Eng yangi kinolarni tomosha qiling!",
                         reply_markup=main_keyboards(user_id=message.from_user.id))
    await state.set_state(UserStates.main)


# Video
@dp.message(F.from_user.id.in_(ADMINS) & F.content_type == "video", AdminStates.send_message)
async def edit_movie(message: Message, state: FSMContext):
    users = users_db.select_all_users()
    real_users = 0
    blocked_users = 0
    for user in users:
        try:
            await bot.send_video(chat_id=user[0], video=message.video.file_id, caption=message.caption)
            await asyncio.sleep(0.3)
            real_users += 1
        except TelegramForbiddenError:
            blocked_users += 1
    await message.answer(text=f"Habar <b>{real_users}</b> ta obunachiga yuborildi\n\n<b>{blocked_users}</b> ta "
                              f"obunachi botni bloklagan\n\nJami obunachilar: {real_users + blocked_users} ta")
    await message.answer(text=f"Eng yangi kinolarni tomosha qiling!",
                         reply_markup=main_keyboards(user_id=message.from_user.id))
    await state.set_state(UserStates.main)

