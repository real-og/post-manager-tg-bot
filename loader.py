from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import logging
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

logging.basicConfig(level=logging.WARNING)
ADMIN_IDS = os.environ.get('ADMIN_IDS').split(',')
BOT_TOKEN = str(os.environ.get('BOT_TOKEN'))

storage = RedisStorage2(db=12)
# storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)