from parrot_integrations.core import generate_update_schema, update_object
from parrot_integrations.context_service.context_types import OBJECT_SCHEMA


def get_schema():
    return generate_update_schema(object_type='context_type', object_schema=OBJECT_SCHEMA, update_fields=[
        'name',
        'description',
        'is_inherited',
        'status_id',
        'content_type',
        'schema',
        'is_encrypted'
    ])


def process(inputs, integration, token, account_uuid, **kwargs):
    return update_object(integration=integration, account_uuid=account_uuid, object_type='context_type',
                         object_uuid=inputs['context_type_uuid'], data=inputs['attributes'], token=token)
