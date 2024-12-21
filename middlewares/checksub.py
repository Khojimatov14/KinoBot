from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext

from keyboards import channels_keyboard
from loader import bot
from states import UserStates
from utils import subscription
from data.config import CHANNELS
from aiogram import BaseMiddleware, types


class Subscription(BaseMiddleware):
    async def __call__(self, handler, update: types.Update, data: dict):

        if update.callback_query and update.callback_query.data == "check_sub":
            return await handler(update, data)
        elif update.message and update.message.text in ["/start", "/bot"]:
            return await handler(update, data)

        user_id = update.message.from_user.id if update.message else update.callback_query.from_user.id

        result = "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling!"
        final_status = True
        non_sub_channels = []
        for channel in CHANNELS:
            status = await subscription(user_id=user_id, channel=channel)
            final_status *= status
            channel = await bot.get_chat(channel)
            if not status:
                non_sub_channels.append(channel)
        if not final_status:
            if update.message:
                await update.message.answer(text=result, reply_markup=channels_keyboard(channels=non_sub_channels))
            elif update.callback_query:
                try:
                    await update.callback_query.message.edit_text(text=result, reply_markup=channels_keyboard(channels=non_sub_channels))
                except TelegramBadRequest:
                    await update.callback_query.message.answer(text=result, reply_markup=channels_keyboard(channels=non_sub_channels))
                    await update.callback_query.message.delete_reply_markup()
            return

        return await handler(update, data)
