import logging

from aiohttp import web

logger = logging.getLogger(__name__)


async def get(request: web.Request) -> web.Response:
    return web.json_response({})
