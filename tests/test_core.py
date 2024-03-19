import uuid


def test_basic_data_formatter():
    from parrot_integrations.core.common import format_data
    complex_key = str(uuid.uuid4())
    inputs = dict(
        complex=dict(path=f'"{complex_key}".val'),
        value=dict(value=True),
        additional_properties_object=[
            dict(key='key1', value='value1'),
            dict(key='key2', value='value2')
        ]
    )
    schema=dict(
        type='object',
        properties=dict(
            additional_properties_object=dict(
                type='object',
                additionalProperties=True,
            )
        )
    )
    record = {
        complex_key: {
            'val': 1
        },
    }
    formatted = format_data(record=record, inputs=inputs, schema=schema)
    expected = dict(
        complex=1,
        value=True,
        additional_properties_object=dict(
            key1='value1',
            key2='value2',
        )
    )
    assert formatted == expected
