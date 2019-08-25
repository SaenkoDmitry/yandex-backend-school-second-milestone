from aiohttp import web
from jsonschema import validate, ValidationError

from app.db.tarantool import citizens_conn
from app.schema.rest import citizens_post_request_schema, citizen_patch_request_schema
from app.schema.tarantool import *
from app.service import service
from app.utils.helper import update_relatives, actualize_dict, convert_dict_to_tuple, convert_tuple_to_dict
from app.utils.validation import format_checker

routes = web.RouteTableDef()


@routes.post('/imports')
async def imports(request):
    data = await request.json()
    try:
        validate(data, citizens_post_request_schema, format_checker=format_checker)
        citizens = data['citizens']
        res = service.imports(citizens)
    except ValidationError:
        return web.HTTPBadRequest()
    return web.json_response(res, status=201)


@routes.patch('/imports/{import_id}/citizens/{citizen_id}')
async def patch(request):
    update_for_citizen = await request.json()
    import_id, citizen_id = request.match_info['import_id'], int(request.match_info['citizen_id'])
    try:
        validate(update_for_citizen, citizen_patch_request_schema, format_checker=format_checker)
        citizen_old = citizens_conn.select((import_id, citizen_id))[0]
        citizen_dict = convert_tuple_to_dict(citizen_old[1:], tarantool_schema_tuple)

        update_relatives(import_id, citizen_dict, update_for_citizen)

        actualize_dict(citizen_dict, update_for_citizen)

        citizen_updated_tuple = convert_dict_to_tuple(citizen_dict, tarantool_schema_tuple)
        citizen_updated_tuple.insert(0, import_id)

        resp = citizens_conn.replace(citizen_updated_tuple)[0]
    except ValidationError:
        return web.HTTPBadRequest()

    return web.json_response({
        'data': dict(zip(tarantool_schema_tuple, resp[1:]))
    })


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
