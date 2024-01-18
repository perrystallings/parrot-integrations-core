def get_details():
    return dict(
        name='Create Account',
        description='Create account based on provided data',
        is_expandable=False,
        schema=dict(
            type='object',
            additionalProperties=False,
            description='Insert Row into BigQuery Table',
            required=['inputs', 'outputs'],
            properties=dict(
                expand_results=dict(
                    type='boolean',
                    default=False,
                    enum=[False]
                ),
                inputs=dict(
                    type='object',
                    additionalProperties=False,
                    required=['project_id', 'dataset_id', 'table_id', 'columns'],
                    properties=dict(
                        parent_uuids=dict(
                            type='object',
                            additionalProperties=False,
                            properties=dict(
                                oneOf=[
                                    dict(
                                        path=dict(
                                            type='string',
                                            minLength=1,
                                        ),
                                        default=dict(
                                            type='array',
                                            items=dict(
                                                type='string',
                                                format='uuid'
                                            )
                                        )
                                    ),
                                    dict(
                                        value=dict(
                                            type='array',
                                            items=dict(
                                                type='string',
                                                format='uuid'
                                            )
                                        )
                                    )
                                ]
                            ),
                        ),
                        name=dict(
                            type='object',
                            additionalProperties=False,
                            properties=dict(
                                oneOf=[
                                    dict(
                                        path=dict(
                                            type='string',
                                            minLength=1,
                                        ),
                                        default=dict(
                                            type='string',
                                        )
                                    ),
                                    dict(
                                        value=dict(
                                            type='string',
                                        )
                                    )
                                ]
                            ),
                        ),
                        account_type_uuid=dict(
                            type='object',
                            additionalProperties=False,
                            properties=dict(
                                oneOf=[
                                    dict(
                                        path=dict(
                                            type='string',
                                            minLength=1,
                                        ),
                                        default=dict(
                                            type='string',
                                            format='uuid'
                                        )
                                    ),
                                    dict(
                                        value=dict(
                                            type="string",
                                            format='uuid'
                                        ),

                                    )
                                ]
                            ),
                        ),
                        extra_attributes=dict(
                            type='object',
                            additionalProperties=False,
                            properties=dict(
                                oneOf=[
                                    dict(
                                        path=dict(
                                            type='string',
                                            minLength=1,
                                        ),
                                        default=dict(
                                            type='object',
                                        )
                                    ),
                                    dict(
                                        value=dict(
                                            type='object',
                                        )
                                    )
                                ]
                            )
                        ),
                    )
                ),
                outputs=dict(
                    type='object',
                    required=[
                        'account_uuid'
                        'parent_uuids',
                        'name',
                        'created_ts'
                    ],
                    properties=dict(
                        account_uuid=dict(
                            type='string',
                        ),
                        parent_uuids=dict(
                            type='array',
                            items=dict(
                                type='string',
                                format='uuid'
                            )
                        ),
                        name=dict(
                            type='string'
                        ),
                        created_ts=dict(
                            type='integer',
                        )
                    )
                ),
            )
        )
    )


def process(workflow_uuid, account_uuid, node_uuid, trigger_uuid, ingested_ts, processed_ts, inputs, integration,
            **kwargs):
    pass