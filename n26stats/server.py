from aiohttp import web

from n26stats import routes


def create_application() -> web.Application:
    application = web.Application()
    routes.init(application)
    return application
