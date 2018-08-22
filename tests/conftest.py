from decimal import Decimal
from typing import Callable, Dict

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
from asynctest import CoroutineMock
from pytest_mock import MockFixture

from n26stats import stats
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


@pytest.fixture(autouse=True)
def reset_stats_container(mocker: MockFixture) -> None:
    mocker.patch.object(
        stats,
        'stats_container',
        return_value=stats.StatsContainer()
    )


@pytest.fixture
def stats_empty() -> Dict:
    return {
        'avg': Decimal(0),
        'count': 0,
        'max': Decimal(0),
        'min': Decimal(0),
        'sum': Decimal(0),
    }


@pytest.fixture
def stats_api_empty() -> Dict:
    return {
        'avg': '0.00',
        'count': 0,
        'max': '0.00',
        'min': '0.00',
        'sum': '0.00',
    }
