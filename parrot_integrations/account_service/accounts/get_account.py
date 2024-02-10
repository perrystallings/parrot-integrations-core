from parrot_integrations.account_service.accounts import SCHEMA
from parrot_integrations.core.integrations import get_object, generate_get_schema

def get_schema():
    return generate_get_schema(object_type='account', object_schema=SCHEMA)

def process(inputs, integration, token, account_uuid, **kwargs):
    return get_object(integration=integration, object_type='account', object_uuid=inputs['account_uuid'], token=token, account_uuid=account_uuid)
