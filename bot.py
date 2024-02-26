from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client
import asyncio
pyrogram_bot = Client("bot_session", config.API_ID, config.API_HASH, bot_token=config.TOKEN, workers=10,
    max_concurrent_transmissions=10)
bot = Bot(config.TOKEN, loop=pyrogram_bot.loop)
async def get_username():
    bot_info = await bot.get_me()
    username = bot_info.username
    return username
loop = asyncio.get_event_loop()
username = loop.run_until_complete(get_username())

dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()