import asyncio
import logging
import sys

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, WEBHOOK_PORT
from database.database import close_db, init_db
from database.seeds import seed_all
from handlers.payments import router as payments_router
from handlers.profile import router as profile_router
from handlers.quiz import router as quiz_router
from handlers.start import router as start_router
from middlewares.access import DbSessionMiddleware
from webapp.webhook import create_web_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


def setup_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(DbSessionMiddleware())
    dp.callback_query.middleware(DbSessionMiddleware())
    dp.pre_checkout_query.middleware(DbSessionMiddleware())

    dp.include_router(start_router)
    dp.include_router(quiz_router)
    dp.include_router(profile_router)
    dp.include_router(payments_router)

    return dp


async def main():
    await init_db()
    await seed_all()
    logger.info("Database initialized and seeded.")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = setup_dispatcher()

    app = create_web_app(bot)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=WEBHOOK_PORT)
    await site.start()
    logger.info("Webhook server started on port %s", WEBHOOK_PORT)

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        logger.info("Bot polling started.")
        await dp.start_polling(bot)
    finally:
        await runner.cleanup()
        await close_db()
        logger.info("Shutdown complete.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
        sys.exit(0)
