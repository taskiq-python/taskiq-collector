from pathlib import Path
from typing import Any, AsyncGenerator

import pytest
from alembic.config import main as migrate
from fastapi import FastAPI
from httpx import AsyncClient

from taskiq_collector.db.config import database
from taskiq_collector.web.application import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(autouse=True)
async def initialize_db() -> AsyncGenerator[None, None]:
    """
    Create models and databases.

    :yield: new engine.
    """
    conf_file = Path(__file__).parent / "alembic.ini"
    migrate(["-c", str(conf_file), "--raiseerr", "upgrade", "head"])

    await database.connect()

    yield

    await database.disconnect()

    migrate(["-c", str(conf_file), "--raiseerr", "downgrade", "base"])


@pytest.fixture
def fastapi_app() -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app(add_prometheus=False)
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
