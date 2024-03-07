from parrot_integrations.core import generate_update_schema, update_object
from parrot_integrations.approval_service.submissions import OBJECT_SCHEMA


def get_schema():
    return generate_update_schema(object_type='submission', object_schema=OBJECT_SCHEMA, update_fields=['status_id',])


def process(inputs, integration, token, account_uuid, **kwargs):
    return update_object(integration=integration, account_uuid=account_uuid, object_type='submission',
                         object_uuid=inputs['submission_uuid'], data=inputs['attributes'], token=token)
