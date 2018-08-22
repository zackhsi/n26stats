import logging

from aiohttp import web

from n26stats.resources import transactions

logger = logging.getLogger(__name__)


def init(app: web.Application) -> None:
    app.router.add_post('/transactions', transactions.post)
    app.router.add_get('/transactions', transactions.get)
    app.router.add_delete('/transactions', transactions.delete)
    logger.info(f'Initialized routes!')
