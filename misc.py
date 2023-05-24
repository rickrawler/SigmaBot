import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.dialects.oracle.dictionary import all_users

registered_users = {

}

all_users = {

}

bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher(bot, storage=MemoryStorage())
