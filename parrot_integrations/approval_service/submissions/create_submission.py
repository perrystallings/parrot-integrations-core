from parrot_integrations.approval_service.submissions import SCHEMA
from parrot_integrations.core.integrations import create_object, generate_create_schema

def get_schema():
    return generate_create_schema(object_type='submission', object_schema=SCHEMA)

def process(inputs, integration, token, account_uuid, **kwargs):
    return create_object(integration=integration, object_type='submission', data=inputs, token=token, account_uuid=account_uuid)
