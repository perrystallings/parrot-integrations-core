import inspect

import pytest

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
