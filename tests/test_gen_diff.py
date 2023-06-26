import pytest
import os
from gendiff.diff import generate_diff


def get_path(file):
    return os.path.join('tests', 'fixtures', file)


@pytest.mark.parametrize(
    "test_input1,test_input2, formatter, expected",
    [
        pytest.param(
            'file1.json',
            'file2.json',
            'stylish',
            'correct_result.txt',
        ),
        pytest.param(
            'file1.yml',
            'file2.yml',
            'stylish',
            'correct_result.txt',
        ),
        pytest.param(
            'file1tree.json',
            'file2tree.json',
            'stylish',
            'correct_result_tree.rtf',
        ),
        pytest.param(
            'file1tree.yml',
            'file2tree.yml',
            'stylish',
            'correct_result_tree.rtf',
        ),
        pytest.param(
            'file1tree.json',
            'file2tree.json',
            'json',
            'correct_json_tree_result.txt',
        ),
        pytest.param(
            'file1tree.json',
            'file2tree.json',
            'plain',
            'correct_plain_tree_result.txt',
        ),
        pytest.param(
            'file1.json',
            'file2.json',
            'plain',
            'correct_plain_flat_result.txt',
        ),
    ],
)
def test_generate_diff(test_input1, test_input2, formatter, expected):
    expected_path = get_path(expected)
    with open(expected_path, 'r') as file:
        result_data = file.read()
        test_path1 = get_path(test_input1)
        test_path2 = get_path(test_input2)
        assert generate_diff(test_path1, test_path2, formatter) == result_data
