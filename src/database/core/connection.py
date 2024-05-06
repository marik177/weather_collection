from src.config import settings

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=True)


DEFAULT_SESSION_FACTORY = async_sessionmaker(
    bind=create_async_engine(
        settings.DATABASE_URL,
        future=True,
        echo=False,
    ),
    expire_on_commit=False,
)
