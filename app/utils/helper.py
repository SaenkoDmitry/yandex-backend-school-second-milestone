from app.db.tarantool import citizens_conn
from app.service import service


def update_relatives(import_id, citizen_dict, update_for_citizen):
    a = set(citizen_dict['relatives'])
    b = set(update_for_citizen['relatives'])
    for relative_id in a.difference(b):
        print('import_id', import_id, 'relative_id', relative_id, 'citizen_dict[citizen_id]', citizen_dict['citizen_id'])
        service.delete_by_relative_id(import_id, relative_id, citizen_dict['citizen_id'])
        # todo : make delete for every i

    for relative_id in b.difference(a):
        print('import_id', import_id, 'relative_id', relative_id, 'citizen_dict[citizen_id]', citizen_dict['citizen_id'])
        service.add_by_relative_id(import_id, relative_id, citizen_dict['citizen_id'])
        # todo : make add for every i


    # todo : need to think out mechanism for convert to dict from tuple and other


def actualize_dict(new_dict, old_dict):
    for k, v in old_dict.items():
        new_dict[k] = v


def convert_dict_to_tuple(old_dict, schema):
    return [old_dict[key] for key in schema]


def convert_tuple_to_dict(old_tuple, schema):
    return dict(zip(schema, old_tuple))
