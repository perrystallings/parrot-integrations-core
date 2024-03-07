import inspect
import responses
import pytest
import uuid
import jsf
from parrot_integrations.core.common import list_integrations, load_integration_module, list_operations
from parrot_integrations.core.validation import validate_integration, validate_operation

INTEGRATION_KEYS = [f'parrot_integrations.{i}' for i in list_integrations()]
OPERATION_KEYS = [[integration_key, operation_key] for integration_key in INTEGRATION_KEYS for operation_key in
                  list_operations(integration_key=integration_key)]


@pytest.mark.parametrize(['integration_key'], [[i] for i in INTEGRATION_KEYS])
def test_valid_integration_schema(integration_key):
    validate_integration(integration_key=integration_key)


@pytest.mark.parametrize(['integration_key', 'operation_key'], OPERATION_KEYS)
def test_valid_operation_schemas(integration_key, operation_key):
    validate_operation(integration_key=integration_key, operation_key=operation_key)

@pytest.mark.parametrize(['integration_key', 'operation_key'], [i for i in OPERATION_KEYS if i[0].endswith('_service') and not i[1].endswith('created') and not i[1].endswith('updated')])
@responses.activate
def test_integration_process(account_uuid, integration_key, operation_key):
    request_method_mapping = {
        'create': 'POST',
        'update': 'PATCH',
        'delete': 'DELETE',
        'get': 'GET',
        'search': 'POST'
    }
    request_url_mapping = {
        'account': 'http://localhost:8000/api/v1/accounts',
        'account_type': 'http://localhost:8000/api/v1/account_types',
        "comment": "http://localhost:8000/api/v1/comments",
        "submission_type": "http://localhost:8000/api/v1/submission_types",
        "submission": "http://localhost:8000/api/v1/submissions",
        'context': 'http://localhost:8000/api/v1/context',
        'context_type': 'http://localhost:8000/api/v1/context_types',
        'integration': 'http://localhost:8000/api/v1/integrations',
        'integration_type': 'http://localhost:8000/api/v1/integration_types',
        "workflow": "http://localhost:8000/api/v1/workflows",
    }
    method = operation_key.split('.')[-1].split('_')[0]
    object_type = '_'.join(operation_key.split('.')[-1].split('_')[1:])
    if object_type.endswith('s'):
        object_type = object_type[:-1]
    base_url = request_url_mapping[object_type]
    object_id = str(uuid.uuid4())
    if method in ['get', 'update', 'delete']:
        url = f'{base_url}/{object_id}'
    elif method in ['search']:
        url = f'{base_url}/search'
    elif method in ['upload']:
        url = f'{base_url}/{object_id}/upload'
    else:
        url = base_url

    response = generate_response(schema=load_integration_module(integration_key=integration_key, operation_key=operation_key).OBJECT_SCHEMA, num_results=3 if method in ['search'] else 1)
    if len(response) == 1:
        response = response[0]
    responses.add(getattr(responses, request_method_mapping[method]), url, json={'response': response}, status=200)
    integration = load_integration_module(integration_key=integration_key)
    operation = load_integration_module(integration_key=integration_key, operation_key=operation_key)
    inputs = jsf.JSF(operation.get_schema()['schema']['properties']['inputs']).generate()
    if object_id in url:
        inputs[object_type + '_uuid'] = object_id
    operation.process(inputs = inputs, integration=dict(extra_attributes=dict(base_url='http://localhost:8000/api/v1/')), token={'Authorization': 'Bearer token'}, account_uuid=account_uuid, **{'attributes': response, 'context_uuid': object_id, 'context_type_uuid': object_id})

def generate_response(schema, num_results=1):
    from jsf import JSF
    return [JSF(schema).generate() for _ in range(num_results)]
