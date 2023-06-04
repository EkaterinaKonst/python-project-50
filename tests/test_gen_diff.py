from gendiff.some_code import generate_diff
import pytest


fl1 = 'tests/fixtures/file1.json'
fl2 = 'tests/fixtures/file2.json'
result = 'tests/fixtures/correct_result.txt'
read_result_json = open(result, 'r')

fl1_yaml = 'tests/fixtures/file1.yml'
fl2_yaml = 'tests/fixtures/file2.yaml'
read_result_yml = open('tests/fixtures/correct_result.txt', 'r')


def test_gendiff_flat_json():
    assert generate_diff(fl1, fl2) == read_result_json.read()


def test_gendiff_flat_yaml():
    assert generate_diff(fl1_yaml, fl2_yaml) == read_result_yml.read()