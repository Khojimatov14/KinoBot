import os
import asyncio
import pyminizip
from typing import Union
from data import ADMINS
from aiogram.types import FSInputFile


async def subscription(user_id: int, channel: Union[int, str]) -> bool:
    from loader import bot
    member = await bot.get_chat_member(user_id=user_id, chat_id=channel)
    result = member.status in ["member", "administrator", "creator"]
    return result


async def send_zip_data():
    from loader import bot
    input_file = "data/allData.db"
    output_file = "kino_kadr_bot_data_base.zip"
    password = "14081997"
    compression_level = 5
    pyminizip.compress(input_file, None, output_file, password, compression_level)

    await asyncio.sleep(3)
    await bot.send_document(chat_id="@akjjkjkskjddhdhksajdhaksjdhaksdj", document=FSInputFile(output_file))
    try:
        os.remove(path=output_file)
    except FileNotFoundError:
        await bot.send_message(chat_id=ADMINS[0],text="Faylni o'chirishda hatolik yuz berdi!")
