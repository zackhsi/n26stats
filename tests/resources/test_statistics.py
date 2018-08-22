from aiohttp.test_utils import TestClient as _TestClient


async def test_get(client: _TestClient) -> None:
    response = await client.get('/statistics')
    assert response.status == 200
    data = await response.json()
    assert data == {
        'avg': '0',
        'count': 0,
        'max': '0',
        'min': '0',
        'sum': '0',
    }
