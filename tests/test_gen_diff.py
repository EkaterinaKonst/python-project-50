from gendiff.some_code import generate_diff
import pytest

from tests import get_path


@pytest.mark.parametrize(
    "test_input1,test_input2, expected",
    [
        pytest.param(
            'file1.json',
            'file2.json',
            'correct_result.txt',
            id="flat_json_file"
        ),
    ],
)
def test_generare_diff(test_input1, test_input2, expected):
    expected_path = get_path(expected)
    with open(expected_path, 'r') as file:
        result_data = file.read()
        test_path1 = get_path(test_input1)
        test_path2 = get_path(test_input2)
        assert generate_diff(test_path1, test_path2) == result_data