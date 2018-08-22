import logging
from decimal import Decimal

from aiohttp import web

from n26stats import money, stats

logger = logging.getLogger(__name__)


async def get(request: web.Request) -> web.Response:
    current_stats = stats.get()
    for key, value in current_stats.items():
        if isinstance(value, Decimal):
            current_stats[key] = money.format(value)
    return web.json_response(current_stats)
