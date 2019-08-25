citizens_post_request_schema = {
    'type': 'object',
    'properties': {
        'citizens': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'citizen_id': {'type': 'number'},
                    'town': {'type': 'string'},
                    'street': {'type': 'string'},
                    'building': {'type': 'string'},
                    'apartment': {'type': 'number'},
                    'name': {'type': 'string'},
                    'birth_date': {'type': 'string', 'format': 'simple_date'},
                    'gender': {'type': 'string'},
                    'relatives': {
                        'type': 'array',
                        'items': {
                            "type": "number"
                        }
                    },
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
        'town': {'type': 'string'},
        'street': {'type': 'string'},
        'building': {'type': 'string'},
        'apartment': {'type': 'number'},
        'name': {'type': 'string'},
        'birth_date': {'type': 'string', 'format': 'simple_date'},
        'gender': {'type': 'string'},
        'relatives': {
            'type': 'array',
            'items': {
                "type": "number"
            }
        }
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

import_id_returned = {
    'type': 'object',
    'properties': {
        'data': {
            'type': 'object',
            'properties': {
                'import_id': {'type': 'number '}
            }
        }
    },
    'required': ['import_id']
}
