from secondary_script.second_code import first_function, second_function
from utils.utils import test_func
from utils.reference_funcs_01 import test_func as tf


def hello(x):
    print(test_func(first_function(x, 2)))


hello(4)
