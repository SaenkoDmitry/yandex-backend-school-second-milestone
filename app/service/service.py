import uuid
from collections import OrderedDict
from datetime import datetime

from dateutil.relativedelta import relativedelta
from jsonschema import ValidationError
import numpy as np
from app.db.tarantool import citizens_conn
from app.schema.tarantool import tarantool_schema_tuple
from app.utils.check_consistency import check
from app.utils.helper import convert_tuple_to_dict, convert_dict_to_tuple
from utils.sort import get_key


def imports(citizens):
    check(citizens)
    id = uuid.uuid4().__str__()
    for citizen in citizens:
        citizen_tuple = tuple([id]) + tuple([citizen[key] for key in tarantool_schema_tuple])
        citizens_conn.insert(citizen_tuple)
    resp = {
        'data': {
            'import_id': id
        }
    }
    return resp


def get_by_import_id(import_id):
    res = citizens_conn.select(import_id)
    if len(res) == 0:
        raise FileNotFoundError
    return {
        "data": list(map(lambda x: convert_tuple_to_dict(x[1:], tarantool_schema_tuple), res.data))
    }


def delete_by_relative_id(import_id, relative_id, citizen_id):
    relative_from_db = citizens_conn.select((import_id, relative_id))
    if len(relative_from_db) == 0:
        raise ValidationError("relative_id doesn't exist")
    old_dict = convert_tuple_to_dict(relative_from_db[0][1:], tarantool_schema_tuple)
    try:
        old_dict['relatives'].remove(citizen_id)
    except ValueError:
        raise ValidationError("relative_id doesn't exist")
    tuple_res = convert_dict_to_tuple(old_dict, tarantool_schema_tuple)
    tuple_res.insert(0, import_id)
    citizens_conn.replace(tuple_res)


def add_by_relative_id(import_id, relative_id, citizen_id):
    relative_from_db = citizens_conn.select((import_id, relative_id))
    if len(relative_from_db) == 0:
        raise ValidationError("relative_id doesn't exist")
    old_dict = convert_tuple_to_dict(relative_from_db[0][1:], tarantool_schema_tuple)
    if citizen_id not in old_dict['relatives']:
        old_dict['relatives'].append(citizen_id)
    else:
        raise ValidationError("relative_id doesn't exist")
    tuple_res = convert_dict_to_tuple(old_dict, tarantool_schema_tuple)
    tuple_res.insert(0, import_id)
    citizens_conn.replace(tuple_res)


def get_birthdays(import_id):
    by_months = citizens_conn.call('by_months', (import_id,)).data[0]
    for month, val in by_months.items():
        temp = list()
        if type(val) is not list:
            for citizen_id, presents in val.items():
                temp.append({"citizen_id": int(citizen_id), "presents": presents})
        by_months[month] = temp
    return {
        "data": OrderedDict(sorted(by_months.items(), key=lambda x: get_key(x[0])))
    }


def get_percentile_age(import_id):
    by_cities = citizens_conn.call('by_cities', (import_id,)).data[0]
    percentile = list()
    for city, arr in by_cities.items():
        temp = []
        for d in arr:
            temp.append(relativedelta(datetime.utcnow(), datetime.strptime(d, "%d.%m.%Y")).years)
        by_cities[city] = temp
        percentile.append({
            "town": city,
            "p50": np.around(np.percentile(temp, 50), 2),
            "p75": np.around(np.percentile(temp, 75), 2),
            "p99": np.around(np.percentile(temp, 99), 2),
        })
    return {
        "data": percentile
    }
