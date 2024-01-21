import pytest
import os
ROOT_DIRECTORY = os.path.abspath(__file__).replace('conftest.py', '')
def traverse(folder, target_filename, other_filenames=tuple()):
    import os
    test_cases = []
    other_files = dict()
    for other_filename in other_filenames:
        if os.path.isfile(os.path.join(folder, other_filename)):
            other_files[other_filename] = os.path.join(folder, other_filename)
    for i in os.walk(folder):
        print(i)
        if target_filename in i[2]:
            test_case = dict(
                name=i[0].replace(folder, ''),
                target=os.path.join(i[0], target_filename),
                **other_files
            )
            for other_filename in other_filenames:
                if other_filename in i[2]:
                    test_case[other_filename] = os.path.join(i[0], other_filename)
            test_cases.append(test_case)
    return test_cases


@pytest.fixture()
def root_directory():
    import os
    return ROOT_DIRECTORY
