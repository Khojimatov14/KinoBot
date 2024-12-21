from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from data import config
from utils import DatabaseMoviesInfo, DatabaseMovies, DatabaseUsers

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())
movies_info_db = DatabaseMoviesInfo(path_to_db="data/allData.db")
movies_db = DatabaseMovies(path_to_db="data/allData.db")
users_db = DatabaseUsers(path_to_db="data/allData.db")