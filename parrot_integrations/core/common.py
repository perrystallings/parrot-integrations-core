def load_integration_module(integration_key: str, operation_key: str = None):
    from importlib import import_module

    module = import_module(
        name=integration_key if operation_key is None else f'{integration_key}.{operation_key}'
    )
    return module


def format_data(record, schema):
    data = dict()
    for k, v in schema.items():
        if isinstance(v, list):
            value = [format_data(record=record, schema=i) if isinstance(i, dict) else i for i in v]
        elif isinstance(v, dict):
            if all(i in ['value', 'path', 'default', 'transforms'] for i in v.keys()):
                value = extract_value(field=v, record=record)
            else:
                value = {sub_k: extract_value(field=sub_v, record=record) for sub_k, sub_v in v.items()}
        else:
            value = v
        data[k] = value
    return data


def apply_transform(value, transform):
    from parrot_integrations.core import transforms
    value = getattr(transforms, transform['operator'])(value=value, **transform)
    return value


def extract_value(field, record):
    from jsonpath_ng.ext import parse as ng_parse
    value = None
    if 'path' in field.keys():
        result = ng_parse(path=field['path']).find(record)
        if len(result) == 1:
            value = result.value
        elif len(result) > 1:
            if not field.get('use_first_result', True):
                value = [i.value for i in result]
            else:
                value = result[0].value
    elif 'value' in field.keys():
        value = field['value']
    else:
        raise SyntaxError("Must use 'path' or 'value'")
    if value is None and field.get('default'):
        value = field['default']
    for transform in field.get('transforms', []):
        value = apply_transform(value=value, transform=transform)
    return value
