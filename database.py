from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DB_URL: str = "sqlite+aiosqlite:///app.db"

async_engine = create_async_engine(DB_URL)
async_session_maker = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)
Base = declarative_base()


async def get_db():
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close()
