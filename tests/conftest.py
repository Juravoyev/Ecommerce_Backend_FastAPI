import pytest_asyncio

from httpx import AsyncClient
from httpx import ASGITransport

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

from database import Base
from database import get_db

from main import app


TEST_DATABASE_URL = (
    "sqlite+aiosqlite:///./test.db"
)


engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False
)

TestingSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def override_get_db():

    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = (
    override_get_db
)


@pytest_asyncio.fixture(
    scope="session",
    autouse=True
)
async def setup_database():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )

    yield

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.drop_all
        )


@pytest_asyncio.fixture
async def client():

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:

        yield ac
