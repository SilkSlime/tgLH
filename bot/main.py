import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
from handlers import dp, handle_message

async def main() -> None:
    """Main entry point for the bot."""
    logging.info("Starting bot")
    bot = Bot(token=config['TOKEN'], default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.start_polling(bot)
    logging.info("Bot is running")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info("Starting the application")
    asyncio.run(main())
    logging.info("Application finished")
