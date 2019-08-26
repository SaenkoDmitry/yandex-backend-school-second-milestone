
citizen_id_format = {'type': 'number', 'minimum': 0}
town_format = {'type': 'string', 'minLength': 1, 'maxLength': 256, 'pattern': '([0-9]|[а-яА-Я]){1}'}
street_format = {'type': 'string', 'minLength': 1, 'maxLength': 256, 'pattern': '([0-9]|[а-яА-Я]){1}'}
building_format = {'type': 'string', 'minLength': 1, 'maxLength': 256, 'pattern': '([0-9]|[а-яА-Я]){1}'}
apartment_format = {'type': 'number', 'minimum': 0}
name_format = {'type': 'string', 'minLength': 1, 'maxLength': 256}
birthday_format = {'type': 'string', 'format': 'simple_date'}
gender_format = {'type': 'string', 'pattern': '^(male|female)$'}
relatives_format = {
    'type': 'array',
    'items': {
        "type": "number"
    }
}

citizens_post_request_schema = {
    'type': 'object',
    'properties': {
        'citizens': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'citizen_id': citizen_id_format,
                    'town': town_format,
                    'street': street_format,
                    'building': building_format,
                    'apartment': apartment_format,
                    'name': name_format,
                    'birth_date': birthday_format,
                    'gender': gender_format,
                    'relatives': relatives_format,
                },
                'required': ['citizen_id', 'town', 'street', 'building', 'apartment', 'name', 'birth_date', 'gender',
                             'relatives']
            }
        }
    },
    'required': ['citizens']
}

citizen_patch_request_schema = {
    'type': 'object',
    'properties': {
        'town': town_format,
        'street': street_format,
        'building': building_format,
        'apartment': apartment_format,
        'name': name_format,
        'birth_date': birthday_format,
        'gender': gender_format,
        'relatives': relatives_format,
    },
    'anyOf': [
        {'required': ['citizen_id']},
        {'required': ['town']},
        {'required': ['street']},
        {'required': ['building']},
        {'required': ['apartment']},
        {'required': ['name']},
        {'required': ['birth_date']},
        {'required': ['gender']},
        {'required': ['relatives']},
    ]
}

