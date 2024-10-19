import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
import sqlalchemy
from httpx import ASGITransport, AsyncClient
from pytest import Item
from pytest_asyncio import is_async_test
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from app.core import database_session
from app.core.config import get_settings
from app.core.security.jwt import create_jwt_token
from app.core.security.password import get_password_hash
from app.main import app as fastapi_app
from app.models import Base, User

default_user_id = "b75365d9-7bf9-4f54-add5-aeab333a087b"
default_user_email = "geralt@wiedzmin.pl"
default_user_password = "geralt"
default_user_access_token = create_jwt_token(default_user_id).access_token


def pytest_collection_modifyitems(items: list[Item]) -> None:
    """Ensure all tests run in a session scoped event loop

    See Also: https://pytest-asyncio.readthedocs.io/en/latest/how-to-guides/run_session_tests_in_same_loop.html
    """
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)


@pytest_asyncio.fixture(loop_scope="session", autouse=True)
async def fixture_setup_new_test_database() -> None:
    worker_name = os.getenv("PYTEST_XDIST_WORKER", "gw0")
    test_db_name = f"test_db_{worker_name}"

    # create new test db using connection to current database
    conn = await database_session._ASYNC_ENGINE.connect()
    await conn.execution_options(isolation_level="AUTOCOMMIT")
    await conn.execute(sqlalchemy.text(f"DROP DATABASE IF EXISTS {test_db_name}"))
    await conn.execute(sqlalchemy.text(f"CREATE DATABASE {test_db_name}"))
    await conn.close()

    session_mpatch = pytest.MonkeyPatch()
    session_mpatch.setenv("DATABASE__DB", test_db_name)
    session_mpatch.setenv("SECURITY__PASSWORD_BCRYPT_ROUNDS", "4")

    # force settings to use now monkeypatched environments
    get_settings.cache_clear()

    # monkeypatch test database engine
    engine = database_session.new_async_engine(get_settings().sqlalchemy_database_uri)

    session_mpatch.setattr(
        database_session,
        "_ASYNC_ENGINE",
        engine,
    )
    session_mpatch.setattr(
        database_session,
        "_ASYNC_SESSIONMAKER",
        async_sessionmaker(engine, expire_on_commit=False),
    )

    # create app tables in test database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def fixture_clean_get_settings_between_tests() -> AsyncGenerator[None, None]:
    yield

    get_settings.cache_clear()


@pytest_asyncio.fixture(name="default_hashed_password", scope="session")
async def fixture_default_hashed_password() -> str:
    return get_password_hash(default_user_password)


@pytest_asyncio.fixture(name="session", scope="function")
async def fixture_session_with_rollback(
    monkeypatch: pytest.MonkeyPatch,
) -> AsyncGenerator[AsyncSession, None]:
    # we want to monkeypatch get_async_session with one bound to session
    # that we will always rollback on function scope

    connection = await database_session._ASYNC_ENGINE.connect()
    transaction = await connection.begin()

    session = AsyncSession(bind=connection, expire_on_commit=False)

    monkeypatch.setattr(
        database_session,
        "get_async_session",
        lambda: session,
    )

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture(name="client", scope="function")
async def fixture_client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=fastapi_app)  # type: ignore
    async with AsyncClient(transport=transport, base_url="http://test") as aclient:
        aclient.headers.update({"Host": "localhost"})
        yield aclient


@pytest_asyncio.fixture(name="default_user", scope="function")
async def fixture_default_user(
    session: AsyncSession, default_hashed_password: str
) -> User:
    default_user = User(
        user_id=default_user_id,
        email=default_user_email,
        hashed_password=default_hashed_password,
    )
    session.add(default_user)
    await session.commit()
    await session.refresh(default_user)
    return default_user


@pytest.fixture(name="default_user_headers", scope="function")
def fixture_default_user_headers(default_user: User) -> dict[str, str]:
    return {"Authorization": f"Bearer {default_user_access_token}"}
