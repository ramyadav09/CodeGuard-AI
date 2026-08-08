from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Adjust database URL for async driver compatibility
db_url = settings.DATABASE_URL
is_neon = "neon.tech" in db_url
needs_ssl = "sslmode=require" in db_url or is_neon

# asyncpg does NOT accept sslmode / channel_binding in the URL — strip them out
if "?" in db_url:
    base_url, query = db_url.split("?", 1)
    # Remove sslmode param, keep any other params
    params = [
        p
        for p in query.split("&")
        if not p.startswith("sslmode") and not p.startswith("channel_binding")
    ]
    db_url = base_url + ("?" + "&".join(params) if params else "")

# Normalize URL scheme for async drivers
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif db_url.startswith("sqlite://") and not db_url.startswith("sqlite+aiosqlite://"):
    db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://", 1)

# Build connect_args based on driver
connect_args = {}
if "sqlite" in db_url:
    connect_args["check_same_thread"] = False
elif "postgresql" in db_url and needs_ssl:
    # asyncpg accepts ssl as a string 'require' in connect_args
    connect_args["ssl"] = "require"

engine = create_async_engine(db_url, echo=False, future=True, connect_args=connect_args)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
