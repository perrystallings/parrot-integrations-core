from parrot_integrations.core import generate_update_schema, update_object
from parrot_integrations.integration_service.integration_types import OBJECT_SCHEMA


def get_schema():
    return generate_update_schema(object_type='integration_type', object_schema=OBJECT_SCHEMA, update_fields=[
        'name',
        'description',
        'integration_key',
        'status_id',
    ])


def process(inputs, integration, token, account_uuid, **kwargs):
    return update_object(integration=integration, account_uuid=account_uuid, object_type='integration_type',
                         object_uuid=inputs['integration_type_uuid'], data=inputs['attributes'], token=token)
