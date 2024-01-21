import os

from .conftest import traverse


def test_filter_traversal(root_directory):
    assert len(
        traverse(
            folder=os.path.join(root_directory, './mocks/filters/success'),
            target_filename='filter.json',
            other_filenames=['record.json']
        )
    ) > 0

