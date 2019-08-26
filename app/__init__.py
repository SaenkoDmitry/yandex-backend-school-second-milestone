import os
import sys

from jsonschema import ValidationError

sys.path.append(os.path.dirname(__file__))


from aiohttp import web
from app.routes.routes import routes


@web.middleware
async def error_handling_middleware(request, handler):
    try:
        response = await handler(request)
    except ValidationError as ex:
        return web.HTTPBadRequest(text=ex.message)
    return response


async def make_app():
    app = web.Application(middlewares=[error_handling_middleware])
    app.add_routes(routes)
    return app


web.run_app(make_app(), port=8080)
