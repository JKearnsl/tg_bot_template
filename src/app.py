import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage

from config import CONFIG
from filters import UserStatusFilter, BannedFilter, UnconfirmedFilter
from filters.role import RoleFilter, AdminFilter
from handlers.admin import register_admin
from handlers.user import register_user
from middlewares import ServiceMiddleware
from middlewares.auth import AuthMiddleware
from middlewares.db import DbMiddleware
from middlewares.role import RoleMiddleware

from models import tables
from db import engine, async_session

logger = logging.getLogger(__name__)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(tables.Base.metadata.create_all(bind=engine))
        await conn.run_sync(tables.Base.metadata.create_all)


def get_db_session():
    return async_session  # TODO возможно переписать


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    await init_db()
    logger.error("Starting bot")
    config = CONFIG

    if config.tg_bot.use_redis:
        storage = RedisStorage()
    else:
        storage = MemoryStorage()

    session = get_db_session()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(DbMiddleware(session))
    dp.middleware.setup(ServiceMiddleware())  # TODO: возможно стоит передать тип фабрики в конструктор
    dp.middleware.setup(AuthMiddleware())
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_id))  # todo: упростить

    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(UserStatusFilter)
    dp.filters_factory.bind(BannedFilter)
    dp.filters_factory.bind(UnconfirmedFilter)

    register_admin(dp)
    register_user(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


def app():
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")


if __name__ == '__main__':
    app()
