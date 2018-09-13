forms = {
            'resource_methods': ['GET', 'POST'],
            'item_methods': [ 'GET', 'PUT', 'PATCH', 'DELETE' ],
            'allowed_roles': ['superuser', 'admin'],
            'schema': {
                'version': {
                    'type': 'string'
                },
                'owner': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'accounts',
                        'field': '_id',
                    },
                    'required': True
                },
                'name': {
                    'type': 'string',
                    'minlength': 5
                },
                'office': {
                    'type': 'string',
                    'allowed': ['']
                }
            }
        }
