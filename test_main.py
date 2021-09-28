# Content
import pandas as pd
import numpy as np
from unittest.mock import patch
import pytest
from main import *

def test_remove_duplicate_values(duplicate_list,no_duplicate_list):
    """
    Assert remove_duplicate returns a given list without duplicates. 
    """

    assert all(i == j for i, j in zip(remove_duplicate(duplicate_list), no_duplicate_list))

def test_remove_duplicate_types():
    """
    Assert that type error is raised.
    """
    with pytest.raises(Exception) as excinfo:
        remove_duplicate(1)

    print(excinfo)

    assert f"{type(1)}" in str(excinfo.value)

def test_permutations_1_item(permutations_1_item) :
    """
    Test that permutation function return good output with a 1-size test string.
    """
    assert [permutations_1_item]==permutations(permutations_1_item)

def test_permutations_3_item(output_permutations_3_items,permutations_3_item) :
    """
    Test that permutation function return good output with a 3-size test string.
    """

    assert set(output_permutations_3_items)==set(permutations(permutations_3_item))

def test_determinant_2x2matrix(matrix) :
    """
    Test that the calculation of the determinant is correct
    """

    assert np.round(np.linalg.det(matrix),decimals=5)==compute_determinant(matrix)

def test_max_operation(operators, operands) :
    """
    Assert that the max operation return the good result. 
    """
    
    test_result = maxminexp(list_num=operands, list_op=operators)

    assert test_result[1] == 43


@pytest.fixture
def duplicate_list() :
    return [0,1,2,3,'a',4,5,'a',10,15,10,20]

@pytest.fixture
def no_duplicate_list() :
    return [0,1,2,3,'a',4,5,10,15,20]


@pytest.fixture
def permutations_1_item() :
    return '1'

@pytest.fixture
def permutations_3_item() :
    return '123'

@pytest.fixture
def output_permutations_3_items() :
    return ['123','132','213','231','312','321']

@pytest.fixture
def matrix() :
    return np.array([[-1,2],[3,-1]])

@pytest.fixture
def operands() :
    return [0.6,0.2,0.1,7]

@pytest.fixture()
def operators() :
    return ['/','-','*']