import asyncio
import logging
import sys
from os import getenv
import json
from time import time
from pathlib import Path
from dataclasses import dataclass
from uuid import uuid4
from datetime import datetime

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

MEDIA = Path("/data")
TOKEN = getenv("TOKEN")
dp = Dispatcher()

def dt() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

def ext(file_path: str) -> str:
    return Path(file_path).suffix

def get_topic_name(message: Message) -> str:
    if not message.chat.is_forum:
        return ""
    if message.reply_to_message is None:
        return ""
    if message.reply_to_message.forum_topic_created is None:
        return ""
    if message.reply_to_message.forum_topic_created.name is None:
        return ""
    return message.reply_to_message.forum_topic_created.name

async def get_file_id(message: Message) -> str | None:
    if message.photo:
        return message.photo[-1].file_id
    elif message.video:
        return message.video.file_id
    elif message.document:
        return message.document.file_id
    else:
        return None

async def get_stem(message: Message) -> str:
    filename = ""
    if message.photo:
        filename = "p"
    elif message.video:
        filename = "v"
    elif message.document:
        if message.document.file_name:
            ofn = Path(message.document.file_name).stem
            filename = f"d_{ofn}"
        else:
            filename = f"d"
    else:
        filename = "u"
    return filename

async def get_file_name(stem: str, suffix: str) -> str:
    filename = f"{stem}_{dt()}{suffix}"
    while (MEDIA / filename).exists():
        filename = f"{stem}_{dt()}{suffix}"
    return MEDIA / filename


async def save_media(message: Message) -> None:
    logging.info("Saving media")
    file_id = await get_file_id(message)
    logging.info(f"File id: {file_id}")
    if file_id is None:
        return
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    logging.info(f"File path: {file_path}")
    if file_path is None:
        return
    stem = await get_stem(message)
    filename = await get_file_name(stem, ext(file_path))

    logging.info(f"Filename: {filename}")    
    await message.bot.download_file(file_path, filename, 600)
    logging.info("Media saved")


@dp.message()
async def any_message(message: Message) -> None:
    topic = get_topic_name(message)
    logging.info(f"Get message in topic {topic}")
    if topic == "Save":
        await save_media(message)
        await message.delete()
    else:
        logging.info(f"Unhandled topic {topic}")
    # print(json.dumps(message.__dict__, indent=4, default=str))
        


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())