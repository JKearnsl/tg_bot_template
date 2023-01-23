import urllib.parse

from sqlalchemy import TypeDecorator, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import CONFIG

config = CONFIG


engine = create_async_engine(
    "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(
        user=urllib.parse.quote_plus(config.db.postgresql.username),
        password=urllib.parse.quote_plus(config.db.postgresql.password),
        host=config.db.postgresql.host,
        port=config.db.postgresql.port,
        database=config.db.postgresql.database
    ),
    echo=True,
    future=True
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class IntEnum(TypeDecorator):
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).
    """
    impl = Integer

    def __init__(self, enumtype, *args, **kwargs):
        super(IntEnum, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)
