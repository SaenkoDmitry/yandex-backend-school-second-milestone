from aiohttp import web
from jsonschema import validate

from app.schema.rest import citizens_post_request_schema, citizen_patch_request_schema
from app.service import service
from app.utils.validation import format_checker

routes = web.RouteTableDef()


@routes.post('/imports')
async def imports(request):
    data = await request.json()
    validate(data, citizens_post_request_schema, format_checker=format_checker)
    citizens = data['citizens']
    res = service.imports(citizens)
    return web.json_response(res, status=201)


@routes.patch('/imports/{import_id}/citizens/{citizen_id}')
async def patch(request):
    update_for_citizen = await request.json()
    import_id, citizen_id = request.match_info['import_id'], int(request.match_info['citizen_id'])
    validate(update_for_citizen, citizen_patch_request_schema, format_checker=format_checker)
    data = service.patch(import_id, citizen_id, update_for_citizen)
    return data


@routes.get('/imports/{import_id}/citizens')
async def get_by_import_id(request):
    import_id = request.match_info['import_id']
    try:
        data = service.get_by_import_id(import_id)
    except FileNotFoundError:
        return web.HTTPNotFound
    return web.json_response(data)


@routes.get('/imports/{import_id}/citizens/birthdays')
async def get_birthdays(request):
    import_id = request.match_info['import_id']
    data = service.get_birthdays(import_id)
    return web.json_response(data)


@routes.get('/imports/{import_id}/towns/stat/percentile/age')
async def get_percentile_age(request):
    import_id = request.match_info['import_id']
    data = service.get_percentile_age(import_id)
    return web.json_response(data)
