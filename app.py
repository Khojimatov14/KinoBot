import sys
import asyncio
import logging
import middlewares, filters, handlers
from middlewares import ThrottlingMiddleware
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from loader import dp, bot, movies_info_db, movies_db, users_db


async def main():
    await on_startup_notify()
    await set_default_commands()
    dp.update.middleware.register(ThrottlingMiddleware())

    try:
        movies_info_db.create_table_movies_info()
    except Exception as err:
        print(err)
    try:
        movies_db.create_table_movies()
    except Exception as err:
        print(err)
    try:
        users_db.create_table_users()
    except Exception as err:
        print(err)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
