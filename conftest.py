from typing import AsyncGenerator

import httpx
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import close_all_sessions

from app.db.database import Base  # SQLAlchemy Base
from app.db.database import get_session  # FastAPI dep override
from app.main import app  # FastAPI instance

# -------------- database fixture (SQLite in‑memory) -------------
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DB_URL, echo=False, future=True)
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


# ───────────────────────── session-wide DB setup/teardown ──────────────────────
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    close_all_sessions()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# ───────────────────────── per-test AsyncSession ───────────────────────────────
@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


# ───────────────────────── FastAPI test client ─────────────────────────────────
@pytest_asyncio.fixture
async def client(db: AsyncSession):
    async def _get_test_db():
        yield db

    app.dependency_overrides[get_session] = _get_test_db
    async with AsyncClient(
        base_url="http://test", transport=httpx.ASGITransport(app=app)
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


# -------------- faker as simple data generator -------------------
from faker import Faker


@pytest.fixture(scope="session")
def faker():
    return Faker()
