from aiohttp.test_utils import TestClient as _TestClient


async def test_post(client: _TestClient) -> None:
    response = await client.post('/transactions')
    data = await response.json()
    assert data == {}


async def test_get(client: _TestClient) -> None:
    response = await client.get('/transactions')
    data = await response.json()
    assert data == {}


async def test_delete(client: _TestClient) -> None:
    response = await client.delete('/transactions')
    data = await response.json()
    assert data == {}
