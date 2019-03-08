"""Lab 7: Recursion, Task 2

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a few nested list functions for you to practice
implementing recursively.
"""
from typing import Union, List


def nested_max(obj: Union[object, List]) -> int:
    """Return the maximum item stored in nested list <obj>.

    You may assume all the items are positive, and calling
    nested_max on an empty list returns 0.

    >>> nested_max(17)
    17
    >>> nested_max([1, 2, [1, 2, [3], 4, 5], 4])
    5
    >>> nested_max([])
    0
    """
    if isinstance(obj, int):
        return obj
    else:
        if len(obj) > 0:
            return 0
        else:
            list_ = []
            for item in obj:
                list_ += [nested_max(item)]
            return max(list_)


def max_length(obj: Union[object, List]) -> int:
    """Return the maximum length of any list in nested list <obj>.

    The *maximum length* of a nested list is defined as:
    1. 0, if <obj> is a number.
    2. The maximum of len(obj) and the lengths of the nested lists contained
       in <obj>, if <obj> is a list.

    >>> max_length(17)
    0
    >>> max_length([1, 2, [1, 2], 4])
    4
    >>> max_length([1, 2, [1, 2, [3], 4, 5], 4])
    5
    """
    if isinstance(obj, int):
        return 0
    else:
        list_ = [len(obj)]
        for item in obj:
            list_ += [max_length(item)]
        return max(list_)

def equal(obj1: Union[object, List], obj2: Union[object, List]) -> bool:
    """Return whether two nested lists are equal, i.e., have the same value.

    Note: order matters.

    >>> equal(17, [1, 2, 3])
    False
    >>> equal([1, 2, [1, 2], 4], [1, 2, [1, 2], 4])
    True
    >>> equal([1, 2, [1, 2], 4], [4, 2, [2, 1], 3])
    False
    """
    if not isinstance(obj1, int) and isinstance(obj2, int):
        for item1, item2 in zip(obj1, obj2):
            equal(item1, item2)
    else:
        return obj1 == obj2



def flatten(lst: Union[int, List]) -> List[int]:
    """Return a list containing all the numbers in <lst>.

    <lst> is a nested list, but the returned list should not be nested.
    The items should appear in the output in the left-to-right order they
    appear in <lst>.

    >>> flatten(5)
    [5]
    >>> flatten([1, [2], 3])
    [1, 2, 3]
    """
    if isinstance(lst, int):
        return [lst]
    else:
        result = []
        for obj in lst:
            result += flatten(obj)
        return result
