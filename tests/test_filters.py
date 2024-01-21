import json
import os

import pytest

from .conftest import traverse, ROOT_DIRECTORY

FILTER_TEST_CASES = [
    *[
        [i, True] for i in traverse(
            folder=os.path.join(ROOT_DIRECTORY, 'mocks/filters/success/'),
            target_filename='filter.json',
            other_filenames=['record.json']
        )
    ], *[
        [i, False] for i in traverse(
            folder=os.path.join(ROOT_DIRECTORY, 'mocks/filters/failure/'),
            target_filename='filter.json',
            other_filenames=['record.json']
        )
    ]
]


def test_positive_case_traversal(root_directory):
    assert len(
        traverse(
            folder=os.path.join(root_directory, 'mocks/filters/success/'),
            target_filename='filter.json',
            other_filenames=['record.json']
        )
    ) > 0


def test_negative_case_traversal(root_directory):
    assert len(
        traverse(
            folder=os.path.join(root_directory, 'mocks/filters/failure/'),
            target_filename='filter.json',
            other_filenames=['record.json']
        )
    ) > 0


@pytest.mark.parametrize(['test_case', 'expected_result'], FILTER_TEST_CASES)
def test_filter_operators(test_case, expected_result):
    from parrot_integrations.core.filters import evaluate_filter
    with open(test_case['record.json'], 'rt') as f:
        record = json.load(f)
    with open(test_case['target'], 'rt') as f:
        filters = json.load(f)
    assert evaluate_filter(
        record=record,
        filters=filters
    ) == expected_result
