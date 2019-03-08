"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple
from block import Block


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class BlobGoal(Goal):
    """A player goal in the game Blocky

    Objective is to create the largest connected blob of this goal's target
    colour, anywhere within the Block.
    """

    def score(self, board: Block) -> int:
        """Return the current score for  Blobgoal on the given board.

        The score is always greater than or equal to 0.
        """
        flat_board = board.flatten()
        visited = []
        for i in range(len(flat_board)):
            visited.append([])
            for j in range(len(flat_board)):
                visited[i].append(-1)

        max_ = 0
        for i in range(len(flat_board)):
            for j in range(len(flat_board)):
                if visited[i][j] == -1:
                    max_ = max(max_, self._undiscovered_blob_size((i, j),
                                                                  flat_board,
                                                                  visited))
        return max_

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
           -1  if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        if not check_in_bounds(pos, board):
            return 0
        elif visited[pos[0]][pos[1]] == 0 or visited[pos[0]][pos[1]] == 1:
            return 0
        elif board[pos[0]][pos[1]] != self.colour:
            visited[pos[0]][pos[1]] = 0
            return 0
        else:
            visited[pos[0]][pos[1]] = 1
            count = 1
            right, bottom = (pos[0]+1, pos[1]), (pos[0], pos[1]+1)
            left, up = (pos[0]-1, pos[1]), (pos[0], pos[1]-1)
            count += self._undiscovered_blob_size(right, board, visited)
            count += self._undiscovered_blob_size(bottom, board, visited)
            count += self._undiscovered_blob_size(up, board, visited)
            count += self._undiscovered_blob_size(left, board, visited)
            return count

    def description(self):
        """Return a description of this goal.
        """
        return "Create the largest connnected blob of the target colour"


def check_in_bounds(pos: Tuple[int, int],
                    board: List[List[Tuple[int, int, int]]]) -> bool:
    """
    Check if position is within the bounds of board and there
    are no negatives
    """
    return 0 <= pos[0] < len(board) and 0 <= pos[1] < len(board)


class PerimeterGoal(Goal):
    """A goal to have most amount of blob that is of target colour
    at outer perimeter of board.
    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        flat_board = board.flatten()
        count = 0
        for i in range(len(flat_board)):
            if flat_board[0][i] == self.colour:
                count += 1
            if flat_board[-1][i] == self.colour:
                count += 1
        for i in range(len(flat_board)):
            if flat_board[i][0] == self.colour:
                count += 1
            if flat_board[i][-1] == self.colour:
                count += 1
        return count

    def description(self):
        """Return a description of this goal.
        """
        return "Most possible units of target colour at borders of board"


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })
