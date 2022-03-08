import pytest
import pandas as pd

def GetList(input_string):
    output_list = input_string.split(',')
    for i in range(len(output_list)):
        output_list[i] = output_list[i].strip()
    return output_list

def GetNames(input_list):
    name_list = [x.split()[0] for x in input_list]
    return name_list

# class TestString:
#     def __init__(self, str, expected_list):
#         self.str = str
#         self.expected_list = expected_list

# @pytest.fixture
# def string_tests():
#     return [TestString('a, b', ['a', 'b']), 
#         ...]

def test_split_string_into_list():
    string_test = 'a, b'
    list_test = GetList(string_test)
    assert len(list_test) == 2
    assert list_test[0] == 'a'
    assert list_test[1] == 'b'

def test_split_string_into_list_without_space_after_comma():
    string_test = 'a,b'
    list_test = GetList(string_test)
    assert len(list_test) == 2
    assert list_test[0] == 'a'
    assert list_test[1] == 'b'

def test_split_string_into_list_name_surname():
    string_test = 'n1 c1, n2 c2'
    list_test = GetList(string_test)
    assert len(list_test) == 2
    assert list_test[0] == 'n1 c1'
    assert list_test[1] == 'n2 c2'

def test_getting_name():
    string_test = 'n1 c1, n2 c2'
    list_test = GetList(string_test)
    name1 = GetNames(list_test)
    assert name1[0] == 'n1'
    assert name1[1] == 'n2'

# def test_creating_columns_for_names():