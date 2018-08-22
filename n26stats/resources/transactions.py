import logging
from datetime import datetime, timedelta
from decimal import Decimal

from aiohttp import web

from n26stats import stats
from n26stats.exceptions import StatInTheFuture, StatTooOld

logger = logging.getLogger(__name__)


async def post(request: web.Request) -> web.Response:
    data = await request.json()
    amount = Decimal(data['amount'])
    timestamp = data['timestamp']
    ts = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    try:
        stats.add(amount, ts)
    except StatTooOld:
        status = 204
    except StatInTheFuture:
        status = 422
    else:
        status = 201
        stats.sweep_at(ts + timedelta(seconds=60))
    return web.Response(status=status)


async def delete(request: web.Request) -> web.Response:
    stats.reset()
    return web.Response(status=204)
