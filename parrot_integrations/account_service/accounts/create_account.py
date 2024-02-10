from parrot_integrations.account_service.accounts import SCHEMA
from parrot_integrations.core.integrations import create_object, generate_create_schema

def get_schema():
    return generate_create_schema(object_type='account', object_schema=SCHEMA)

def process(inputs, integration, token, account_uuid, **kwargs):
    return create_object(integration=integration, object_type='account', data=inputs, token=token, account_uuid=account_uuid)
