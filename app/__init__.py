import os
import sys

sys.path.append(os.path.dirname(__file__))


from aiohttp import web
from app.routes.routes import routes


async def make_app():
    app = web.Application()
    app.add_routes(routes)
    return app


web.run_app(make_app(), port=8080)
