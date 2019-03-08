"""Lab 8: Trees and Recursion, Tasks 1 & 2

=== CSC148 Fall 2016 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains a few Tree methods that you should implement recursively.
Make sure you understand both the theoretical idea of trees, as well as how
we represent them in our Tree class.
"""
import random  # For Task 2
from typing import Optional, List, Union, Tuple


class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and LinkedListRec
    from Lab 7; the only major difference is that _rest
    has been replaced by _subtrees to handle multiple
    recursive sub-parts.
    """
    # === Private Attributes ===
    # The item stored at this tree's root, or None if the tree is empty.
    _root: Optional[object]
    # The list of all subtrees of this tree.
    _subtrees: List['Tree']

    # === Representation Invariants ===
    # - If self._root is None then self._subtrees is an empty list.
    #   This setting of attributes represents an empty Tree.
    # - self._subtrees may be empty when self._root is not None.
    #   This setting of attributes represents a tree consisting of just one
    #   node.

    def __init__(self, root: object, subtrees: List['Tree']) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """Return True if this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of nodes contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1
            for subtree in self._subtrees:
                size += subtree.__len__()  # Could also do size += len(subtree)
            return size

    def count(self, item: object) -> int:
        """Return the number of occurrences of <item> in this tree.
        >>> t = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> t.count(3)
        1
        >>> t.count(100)
        0
        """
        if self.is_empty():
            return 0
        else:
            num = 0
            if self._root == item:
                num += 1
            for subtree in self._subtrees:
                num += subtree.count(item)
            return num

    # ------------------------------------------------------------------------
    # Lab Exercises
    # ------------------------------------------------------------------------
    def __contains__(self, item: object) -> bool:
        """Return whether <item> is in this tree.

        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> 1 in t  # Same as t.__contains__(1)
        True
        >>> 5 in t
        True
        >>> 4 in t
        False
        """
        if self._root == item:
            return True
        else:
            for tree in self._subtrees:
                if item in tree:
                    return True
            return False

    def leaves(self) -> list:
        """Return a list of all of the leaf items in the tree.

        >>> Tree(None, []).leaves()
        []
        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> t.leaves()
        [2, 5]
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [Tree(6, []), Tree(7, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.leaves()
        [4, 5, 6, 7]
        """
        if self._root is None:
            return []
        elif len(self._subtrees) == 0:
            return [self._root]
        else:
            leaves = []
            for tree in self._subtrees:
                leaves += tree.leaves()
            return leaves

    def branching_factor(self) -> float:
        """Return the average branching factor of this tree.

        Return 0 if this tree is empty or consists of just a single root node.
        Remember to ignore all 0's coming from leaves in this calculation.

        >>> Tree(None, []).branching_factor()
        0.0
        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> t.branching_factor()
        2.0
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [Tree(6, []), Tree(7, []), Tree(8, []), Tree(9, []),\
                          Tree(10, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.branching_factor()
        3.0
        """
        if self._root is not None:
            total_branches, total_non_leaves = self._branching_factor_helper()
            return total_branches / total_non_leaves
        return 0.0

    def _branching_factor_helper(self) -> Tuple[int, int]:
        """Return a tuple (x,y) where:

        x is the total branching factor of all non-leaf nodes in this tree, and
        y is the total number of non-leaf nodes in this tree.
        """
        # TODO: implement this method
        x, y = 0, 0
        if len(self._subtrees) > 0:
            x, y = len(self._subtrees), 1
            for tree in self._subtrees:
                branches, non_leaves = tree._branching_factor_helper()
                x += branches
                y += non_leaves
        return x, y



    def insert(self, item: object) -> None:
        """Insert <item> into this tree using the following algorithm.

            1. If the tree is empty, <item> is the new root of the tree.
            2. If the tree has a root but no subtrees, create a
               new tree containing the item, and make this new tree a subtree
               of the original tree.
            3. Otherwise, pick a random number between 1 and 3 inclusive.
                - If the random number is 3, create a new tree containing
                  the item, and make this new tree a subtree of the original.
                - If the random number is a 1 or 2, pick one of the existing
                  subtrees at random, and *recursively insert* the new item
                  into that subtree.

        >>> t = Tree(None, [])
        >>> t.insert(1)
        >>> 1 in t
        True
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [Tree(6, []), Tree(7, []), Tree(8, []), Tree(9, []),\
                          Tree(10, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.insert(100)
        >>> 100 in t
        True
        """
        # Use the function randint as follows:
        # >>> random.randint(1, 3)
        # 2  # Randomly returns 1, 2, or 3

        if self._root is None:
            self._root = item
        elif len(self._subtrees) == 0:
            self._subtrees.append(Tree(item, []))
        else:
            rand_int = random.randint(1, 3)
            if rand_int == 3:
                self._subtrees.append(Tree(item, []))
            else:
                tree = random.choice(self._subtrees)
                tree.insert(item)

    def biggest(self):
        """
        find biggest item
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [Tree(6, []), Tree(7, [])])
        >>> t = Tree(1, [lt, rt])
        >>> t.biggest()
        7
        """
        if len(self._subtrees) == 0:
            return self._root
        else:
            max_ = self._root
            for tree in self._subtrees:
                if tree.biggest() > max_:
                    max_ = tree.biggest()
            return max_

    def longest_path(self):
        """Return a list of items on the longest possible path between the root
        of this tree and one of its leaves.
        If there is more than one path with the maximum length,
        return the one that ends at the leaf that is furthest to the left.
        If this tree is empty, return an empty list.
        @type self: Tree
        @rtype: list
        >>> lt = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> rt = Tree(3, [])
        >>> t = Tree(1, [lt, rt])
        >>> t.longest_path()
        [1, 2, 4]
        """
        # count = 0
        # ans = [self._root]
        # for subtree in self._subtrees:
        #     if len(subtree.longest_path()) > count:
        #         ans += subtree.longest_path()
        #         count = len(subtree.longest_path())
        # return ans
        if self.is_empty():
            return []
        else:
            max_path = []
            for subtree in self._subtrees:
                new_path = subtree.longest_path()
                if len(new_path) > len(max_path):
                    max_path = new_path
            return [self._root] + max_path


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'random', 'typing', 'python_ta']
    })

    import doctest
    doctest.testmod()
