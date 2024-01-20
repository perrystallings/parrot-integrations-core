def get_details():
    return dict(
        name='',
        description='',
        is_trigger=True ,
        schema=dict(
            type='object',
            additionalProperties=False,
            description='',
            required=['inputs', 'outputs'],
            properties=dict(
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required=[],
                    properties=dict(
                    )
                ),
                outputs=dict(
                    type='object',
                    additionalProperties=True,
                    required=[],
                    properties=dict()
                ),
            )
        )
    )


def process(workflow_uuid, account_uuid, node_uuid, trigger_uuid, ingested_ts, processed_ts, inputs, integration,
            **kwargs):
    pass
