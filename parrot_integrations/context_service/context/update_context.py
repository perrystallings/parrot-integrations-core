from parrot_integrations.core import generate_update_schema, update_object
from parrot_integrations.context_service.context import OBJECT_SCHEMA


def get_schema():
    return generate_update_schema(object_type='context', object_schema=OBJECT_SCHEMA, update_fields=[
        'name',
        'content',
        'extra_attributes',
        'status_id'
    ])


def process(inputs, integration, token, account_uuid, **kwargs):
    return update_object(integration=integration, account_uuid=account_uuid, object_type='context',
                        path_override=f'context/{inputs["context_uuid"]}',
                         object_uuid=inputs['context_uuid'], data=inputs['attributes'], token=token)
