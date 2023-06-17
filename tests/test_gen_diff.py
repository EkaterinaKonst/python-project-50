from gendiff.some_code import stylish
import pytest
import os


def get_path(file):
    return os.path.join('tests', 'fixtures', file)


@pytest.mark.parametrize(
    "test_input1,test_input2, formater,  expected",
    [
        pytest.param(
            'file1.json',
            'file2.json',
            'stylish',
            'correct_result.txt',
            id="flat_json_file"
        ),
        pytest.param(
            'file1.yml',
            'file2.yml',
            'stylish',
            'correct_result.txt',
            id="flat_yaml_file"
        ),
        pytest.param(
            'file1tree.json',
            'file2tree.json',
            'stylish',
            'correct_result_tree.txt',
            id="tree_json_file"
        ),
        pytest.param(
            'file1tree.yml',
            'file2tree.yml',
            'stylish',
            'correct_result_tree.txt',
            id="tree_yaml_file"
        ),
    ],
)


def test_generare_diff(test_input1, test_input2, formater, expected):
    expected_path = get_path(expected)
    with open(expected_path, 'r') as file:
        result_data = file.read()
        test_path1 = get_path(test_input1)
        test_path2 = get_path(test_input2)
        assert stylish(test_path1, test_path2, formater) == result_data