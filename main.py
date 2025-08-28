import argparse
import logging
import os

import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from dotenv import load_dotenv

from configuration import Config
from database.redis_db import RedisDB
from datafile.file_schema import FileSchema
from updating import update

CSV_FILENAME = "data/exportfsm.csv"
BTN_TEXT = "Случайный материал"

kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=BTN_TEXT)]], resize_keyboard=True
)

dp = Dispatcher()

load_dotenv()
TOKEN = os.getenv("TOKEN")

parser = argparse.ArgumentParser()
parser.add_argument("--config", default="config.json", help="*.json configuration filename")

args = parser.parse_args()
config = Config(args.config)

file_schema = FileSchema(
    config.file_column,
    config.file_delimiter,
    config.file_encoding
)
redis_db = RedisDB(
    config.redis_host,
    config.redis_port,
    config.redis_db
)


@dp.message(Command(commands=["start", "help"]))
async def cmd_handler(message: Message):
    await message.answer("А ты уважаешь закон?")
    await asyncio.sleep(1)
    await message.answer("Я - да!")
    await asyncio.sleep(1)
    await message.answer("Поэтому я тебе помогу случайно его не нарушить")
    await asyncio.sleep(1)
    await message.answer(
        f"Просто нажми кнопку \"{BTN_TEXT}\", "
        "и я тебе пришлю случайные сведения, "
        "которые ни в коем случае нельзя искать в интернете... "
        "да и вообще нигде!"
    )
    await asyncio.sleep(0.5)
    await message.answer(
        'Источник: '
        '<a href="https://minjust.gov.ru/ru/extremist-materials/">'
        'Экстремистские материалы'
        '</a>',
        reply_markup=kb,
        parse_mode="HTML",
    )
    logging.debug(f"Command {message.text} executed")


@dp.message(F.text == BTN_TEXT)
async def rnd_material(message: Message):
    try:
        text = await redis_db.rnd()
        await message.answer(text, disable_web_page_preview=True)
        logging.debug(f"Random material sent")
    except RuntimeError as ex:
        logging.error(f"Exception occurred: {ex}")


async def main():
    bot = Bot(TOKEN)
    try:
        await asyncio.gather(
            update(
                config.file_updating_hours,
                redis_db,
                file_schema,
                config.file_url,
                CSV_FILENAME
            ),
            dp.start_polling(bot)
        )
    except KeyboardInterrupt:
        logging.info("Stopped by user")
    finally:
        await dp.stop_polling()


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s [%(process)d | %(thread)d] %(funcName)s ---> %(message)s", level=config.log_level)
    asyncio.run(main())
