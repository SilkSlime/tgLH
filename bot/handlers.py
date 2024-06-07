import logging
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.types import Message, File

from utils import get_file_extension, generate_unique_filename
from config import config

dp = Dispatcher()

async def get_file_from_message(message: Message) -> File:
    """Return the file object from the message if it exists."""
    if message.photo:
        return await message.bot.get_file(message.photo[-1].file_id)
    if message.video:
        return await message.bot.get_file(message.video.file_id)
    if message.document:
        return await message.bot.get_file(message.document.file_id)
    return None

async def get_filename_stem(message: Message) -> str:
    """Generate a filename stem based on the message content."""
    if message.photo:
        return "photo"
    if message.video:
        return "video"
    if message.document:
        return f"document_{Path(message.document.file_name).stem}" if message.document.file_name else "document"
    return "unknown"

async def download_and_save_file(file: File, filename: str) -> None:
    """Download and save the file to the specified filename."""
    await file.bot.download_file(file.file_path, filename, config['DOWNLOAD_TIMEOUT'])

async def save_media(message: Message) -> None:
    """Save media from the message."""
    logging.info("Starting media save process")
    file = await get_file_from_message(message)
    if not file:
        logging.warning("No file found in the message, aborting save")
        return
    
    logging.info(f"File path determined: {file.file_path}")
    file_extension = get_file_extension(file.file_path)
    stem = await get_filename_stem(message)
    filename = generate_unique_filename(Path(config['DOWNLOAD_PATH']), stem, file_extension)
    
    logging.info(f"Downloading and saving file to: {filename}")
    await download_and_save_file(file, filename)
    logging.info(f"Media successfully saved as {filename}")

@dp.message()
async def handle_message(message: Message) -> None:
    """Handle incoming messages and save media if topic is 'Save'."""
    topic = get_topic_name(message)
    logging.info(f"Received message in topic: {topic}")
    if topic == "Save":
        logging.info("Topic is 'Save', proceeding to save media")
        await save_media(message)
        logging.info("Deleting the original message")
        await message.delete()
    else:
        logging.info(f"Unhandled topic: {topic}")

def get_topic_name(message: Message) -> str:
    """Return the topic name of the message if it exists, otherwise return an empty string."""
    if message.chat.is_forum and message.reply_to_message and message.reply_to_message.forum_topic_created:
        return message.reply_to_message.forum_topic_created.name or ""
    return ""
