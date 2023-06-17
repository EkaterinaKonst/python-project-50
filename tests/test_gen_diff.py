from gendiff.some_code import stylish


fl1 = 'tests/fixtures/file1.json'
fl2 = 'tests/fixtures/file2.json'
result1 = 'tests/fixtures/correct_result.txt'
read_result1 = open(result1, 'r')

fl1_yaml = 'tests/fixtures/file1.yml'
fl2_yaml = 'tests/fixtures/file2.yml'
yaml_result = open('tests/fixtures/correct_result.txt', 'r')

stylish_nested1 = 'tests/fixtures/file1tree.json'
stylish_nested2 = 'tests/fixtures/file2tree.json'
stylish_nested_result = open('tests/fixtures/correct_result_tree.txt', 'r')

stylish_nested1_yml = 'tests/fixtures/file1tree.yml'
stylish_nested2_yml = 'tests/fixtures/file2tree.yml'
stylish_nested_result_yml = open('tests/fixtures/correct_result_tree.txt', 'r')


def test_gendiff_flat_json():
    assert stylish(fl1, fl2) == read_result1.read()


def test_gendiff_flat_yml():
    assert stylish(fl1_yaml, fl2_yaml) == yaml_result.read()


def test_stylish_nested_json():
    assert stylishf(stylish_nested1, stylish_nested2) == stylish_nested_result.read()


def test_stylish_nested_yml():
    assert stylish(stylish_nested1_yml, stylish_nested2_yml) == stylish_nested_result_yml.read()
