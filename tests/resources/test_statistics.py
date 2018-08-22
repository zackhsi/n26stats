from datetime import datetime
from decimal import Decimal

import pytest
from aiohttp.test_utils import TestClient as _TestClient

from n26stats import stats


async def test_get_simple(client: _TestClient) -> None:
    response = await client.get('/statistics')
    assert response.status == 200
    data = await response.json()
    assert data == {
        'avg': '0.00',
        'count': 0,
        'max': '0.00',
        'min': '0.00',
        'sum': '0.00',
    }

    stats.add(
        amount=Decimal(1),
        ts=datetime.now(),
    )
    response = await client.get('/statistics')
    assert response.status == 200
    data = await response.json()
    assert data == {
        'avg': '1.00',
        'count': 1,
        'max': '1.00',
        'min': '1.00',
        'sum': '1.00',
    }


@pytest.mark.parametrize(
    ('amount', 'expected_avg'),
    [
        (Decimal('1.005'), '1.00'),
        (Decimal('1.0051'), '1.01'),
    ]
)
async def test_get_rounding(
    client: _TestClient,
    amount: Decimal,
    expected_avg: str,
) -> None:
    stats.add(
        amount=amount,
        ts=datetime.now(),
    )
    response = await client.get('/statistics')
    assert response.status == 200
    data = await response.json()
    assert data['avg'] == expected_avg
