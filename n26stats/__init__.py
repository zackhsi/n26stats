import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s: %(levelname)s %(message)s',
)
logging.getLogger('asyncio').setLevel(logging.WARNING)
