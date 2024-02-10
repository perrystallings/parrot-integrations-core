from urllib.parse import urljoin
import requests

def generate_get_schema(object_type, object_schema):
    return dict(
        name=f'Get {object_type}',
        description=f'Get a single {object_type} by ID.',
        is_trigger=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs'],
            properties=dict(
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required=[f'{object_type}_uuid'],
                    properties={
                        f'{object_type}_uuid': dict(
                            type='string',
                            format='uuid'
                        )
                    }
                ),
                outputs=dict(
                    type='object',
                    additionalProperties=True,
                    required=[object_type, 'exists'],
                    properties={
                        object_type: object_schema,
                        "exists": dict(
                            type='boolean'
                        )
                    }
                ),
            )
        )
    )

def generate_create_schema(object_type, object_schema):
    return dict(
        name=f'Create {object_type}',
        description=f'Create a single {object_type}',
        is_trigger=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs'],
            properties=dict(
                inputs=object_schema,
                outputs=dict(
                    type='object',
                    additionalProperties=True,
                    required=[object_type, 'created'],
                    properties={
                        object_type: object_schema,
                        "created": dict(
                            type='boolean'
                        )
                    }
                ),
            )
        )
    )


def generate_update_schema(object_type, object_schema, update_schema):
    return dict(
        name=f'Update {object_type}',
        description=f'Update a single {object_type}',
        is_trigger=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs'],
            properties=dict(
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required= [f'{object_type}_uuid', 'attributes'],
                    properties= {
                        f'{object_type}_uuid': dict(
                            type='string',
                            format='uuid'
                        ),
                        'attributes': update_schema
                }
                ),
                outputs=dict(
                    type='object',
                    additionalProperties=True,
                    required=[object_type, 'updated'],
                    properties={
                        object_type: object_schema,
                        "updated": dict(
                            type='boolean'
                        )
                    }
                ),
            )
        )
    )


def generate_search_schema(plural_object_type, object_schema, search_schema):
    return dict(
        name=f'Search {plural_object_type}',
        description=f'Search for {plural_object_type}',
        is_trigger=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            required=['inputs'],
            properties=dict(
                inputs=search_schema,
                outputs=dict(
                    type='object',
                    additionalProperties=True,
                    required=[plural_object_type],
                    properties={
                        plural_object_type: dict(
                            type='array',
                            items=object_schema,
                        )
                    }
                ),
            )
        )
    )
def get_object(integration, account_uuid, object_type, object_uuid, token, path_override=None, **kwargs):
    from urllib.parse import urljoin
    import requests
    results = {
        object_type: None,
        "exists": False
    }
    path = path_override if path_override is not None else f'/{object_type}s/{object_uuid}'
    resp = requests.get(urljoin(integration['base_url'], path), headers=token)
    if resp.status_code == 200:
        results['exists'] = True
        results[object_type] = resp.json()['response']
    return results

def create_object(integration, account_uuid, object_type, data, token, path_override=None, **kwargs):
    from urllib.parse import urljoin
    import requests
    results = {
        object_type: None,
        "created": False
    }
    path = path_override if path_override is not None else f'/{object_type}s/'
    resp = requests.post(urljoin(integration['base_url'], path), json=data, headers=token)
    if resp.status_code == 200:
        results['created'] = True
        results[object_type] = resp.json()['response']
    return results

def update_object(integration, account_uuid, object_type, object_uuid, data, token, path_override=None, **kwargs):
    from urllib.parse import urljoin
    import requests
    results = {
        object_type: None,
        "updated": False
    }
    path = path_override if path_override is not None else f'/{object_type}s/{object_uuid}'
    resp = requests.patch(urljoin(integration['base_url'], path), json=data, headers=token)
    if resp.status_code == 200:
        results['updated'] = True
        results[object_type] = resp.json()['response']
    return results
def search_objects(integration, search_parameters, plural_object_type, token, limit=100, **kwargs):
    objects = []
    search = True

    page = 1
    while search:
        payload = dict(
            limit=limit,
            search_parameters=search_parameters
        )
        if limit is not None:
            payload['page'] = page
        resp = requests.post(
            url=urljoin(integration['extra_attributes']['base_url'], f'/{plural_object_type}/search'),
            json=payload,
            headers=token
        )
        objects.extend(resp.json()['response'])
        if limit is None or len(resp.json()['response']) < limit:
            search = False
        page+=1
    return {plural_object_type: objects}
