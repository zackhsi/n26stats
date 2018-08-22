from typing import Callable

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from n26stats.server import create_application
from n26stats.settings import ENVIRONMENT, TESTING

if ENVIRONMENT != TESTING:
    raise RuntimeError(f'Tests can only run if ENVIRONMENT={TESTING}!')


@pytest.fixture
async def application() -> web.Application:
    application = create_application()
    yield application
    await application.shutdown()


@pytest.fixture
async def client(
    application: web.Application,
    aiohttp_client: Callable,
) -> TestClient:
    yield await aiohttp_client(application)
