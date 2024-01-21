import inspect

import pytest

from parrot_integrations.core.common import list_integrations, load_integration_module, list_operations

INTEGRATION_KEYS = [f'parrot_integrations.{i}' for i in list_integrations()]
OPERATION_KEYS = [[integration_key, operation_key] for integration_key in INTEGRATION_KEYS for operation_key in
                  list_operations(integration_key=integration_key)]


@pytest.mark.parametrize(['integration_key'], [[i] for i in INTEGRATION_KEYS])
def test_validate_integration_schema(integration_key):
    integration = load_integration_module(integration_key=integration_key)
    assert hasattr(integration, 'get_schema')
    assert hasattr(integration, 'connect')
    schema_signature = inspect.signature(integration.get_schema)
    connect_signature = inspect.signature(integration.connect)
    assert len(schema_signature.parameters.keys()) == 0
    assert len(connect_signature.parameters.keys()) == 2
    assert 'extra_attributes' in connect_signature.parameters.keys()
    assert 'credentials' in connect_signature.parameters.keys()
    assert integration.get_schema()


@pytest.mark.parametrize(['integration_key', 'operation_key'], OPERATION_KEYS)
def test_valid_operation_schemas(integration_key, operation_key):
    operation = load_integration_module(integration_key=integration_key, operation_key=operation_key)
    assert hasattr(operation, 'get_schema')
    assert hasattr(operation, 'process')
    schema_signature = inspect.signature(operation.get_schema)
    process_signature = inspect.signature(operation.process)
    assert len(schema_signature.parameters.keys()) == 0
    assert operation.get_schema()
    kwarg_parameter = any(i.kind.name == 'VAR_KEYWORD' for i in process_signature.parameters.values())
    for keyword in ['workflow_uuid', 'node_uuid', 'processed_ts', 'inputs', 'integration']:
        assert keyword in process_signature.parameters.keys() or kwarg_parameter
