from typing import Callable

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
from asynctest import CoroutineMock
from pytest_mock import MockFixture

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


@pytest.fixture(autouse=True)
def mock_sweep_at(mocker: MockFixture) -> CoroutineMock:
    mock: CoroutineMock = mocker.patch(
        'n26stats.stats.sweep_at',
        new=CoroutineMock(),
    )
    return mock
