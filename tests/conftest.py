import pytest_asyncio
from database import Base, async_engine, async_session_maker
from httpx import ASGITransport, AsyncClient
from main import app
from models import Recipe


@pytest_asyncio.fixture(autouse=True, loop_scope="session")
async def create_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        recipe = Recipe(title='Test Recipe', cooking_time=2.4, ingredients='Any', description='Just recipe')
        session.add(recipe)
        await session.commit()

    yield

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(loop_scope="session")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture(loop_scope="session")
async def async_db():
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close()
