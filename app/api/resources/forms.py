forms = {
    'resource_methods': ['GET', 'POST', 'DELETE'],
    'public_methods': ['GET'],
    'public_item_methods': ['GET'],
    'item_methods': [ 'GET', 'PUT', 'PATCH', 'DELETE' ],
    'allowed_roles': ['superuser', 'admin'],
    'schema': {
        'version': {
            'type': 'string',
            'required': True
        },
        'owner': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'accounts',
                'field': '_id',
                'embeddable': True
            },
            'required': True
        },
        'name': {
            'type': 'string',
            'minlength': 5,
            'required': True
        },
        'office': {
            'type': 'string',
            'allowed': ['smped', 'smdhc'],
            'required': True
        },
        'activity': {
            'type': 'string',
            'required': True
        },
        'fields': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    '_id': {
                        'type': 'objectid',
                        'default_setter': 'generateid',
                        'required': True
                    },
                    'label': {
                        'type': 'string',
                        'required': True,
                    },
                    'type': {
                        'type': 'string',
                        'allowed': ['number', 'text'],
                        'required': True
                    },
                    'required': {
                        'type': 'boolean',
                        'required': True
                    },
                    'order': {
                        'type': 'integer',
                        'required': True
                    }
                }
            }
        }
    }
}
