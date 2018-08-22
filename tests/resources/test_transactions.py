from datetime import datetime

import pytest
from aiohttp.test_utils import TestClient as _TestClient
from asynctest import CoroutineMock
from freezegun import freeze_time


@freeze_time(datetime(year=2018, month=10, day=17, hour=0, minute=2, second=0))
@pytest.mark.parametrize(
    ('timestamp', 'expected_status'),
    [
        ('2018-10-17T00:02:00.000Z', 201),  # Success.
        ('2018-10-17T00:01:00.000Z', 201),  # Success.
        ('2018-10-17T00:00:00.000Z', 204),  # Too old.
        ('2018-10-17T00:03:00.000Z', 422),  # In the future.
    ]
)
async def test_post(
    client: _TestClient,
    mock_sweep_at: CoroutineMock,
    timestamp: str,
    expected_status: int,
) -> None:
    mock_sweep_at.reset_mock()
    response = await client.post(
        '/transactions',
        json={
            'amount': '12.3343',
            'timestamp': timestamp,
        }
    )
    assert response.status == expected_status
    if expected_status == 201:
        assert mock_sweep_at.called
    else:
        assert not mock_sweep_at.called


async def test_delete(client: _TestClient) -> None:
    response = await client.delete('/transactions')
    data = await response.json()
    assert data == {}
