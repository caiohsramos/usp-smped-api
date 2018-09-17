answers = {
    'resource_methods': ['GET', 'POST'],
    'item_methods': ['GET', 'PUT', 'PATCH', 'DELETE'],
    'allowed_roles': ['superuser', 'admin'],
    'schema': {
        'form_id': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'forms',
                'field': '_id',
                'embeddable': True
            },
            'required': True
        },
        'email': {
            'type': 'string',
            'regex': r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
            'required': True,
        },
        'values': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'field_id': {
                        'type': 'objectid',
                        'required': True
                    },
                    'value': {
                        'type': ['string','number'],
                        'required': True
                    }
                }
            }
        }
    }
}
