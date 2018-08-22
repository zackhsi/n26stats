import logging

from aiohttp import web

logger = logging.getLogger(__name__)


async def post(request: web.Request) -> web.Response:
    return web.json_response({})


async def get(request: web.Request) -> web.Response:
    return web.json_response({})


async def delete(request: web.Request) -> web.Response:
    return web.json_response({})
