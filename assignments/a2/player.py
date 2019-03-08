"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the player class hierarchy.
"""

import random
from typing import Optional, Tuple
import pygame
from renderer import Renderer
from block import Block
from goal import Goal

TIME_DELAY = 600


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    renderer:
        The object that draws our Blocky board on the screen
        and tracks user interactions with the Blocky board.
    id:
        This player's number.  Used by the renderer to refer to the player,
        for example as "Player 2"
    goal:
        This player's assigned goal for the game.
    """
    renderer: Renderer
    id: int
    goal: Goal

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.renderer = renderer
        self.id = player_id

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.
        """
        raise NotImplementedError


class HumanPlayer(Player):
    """A human player.

    A HumanPlayer can do a limited number of smashes.

    === Public Attributes ===
    num_smashes:
        number of smashes which this HumanPlayer has performed
    === Representation Invariants ===
    num_smashes >= 0
    """
    # === Private Attributes ===
    # _selected_block
    #     The Block that the user has most recently selected for action;
    #     changes upon movement of the cursor and use of arrow keys
    #     to select desired level.
    # _level:
    #     The level of the Block that the user selected
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0

    # The total number of 'smash' moves a HumanPlayer can make during a game.
    MAX_SMASHES = 1

    num_smashes: int
    _selected_block: Optional[Block]
    _level: int

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        super().__init__(renderer, player_id, goal)
        self.num_smashes = 0

        # This HumanPlayer has done no smashes yet.
        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._selected_block = None

    def process_event(self, board: Block,
                      event: pygame.event.Event) -> Optional[int]:
        """Process the given pygame <event>.

        Identify the selected block and mark it as highlighted.  Then identify
        what it is that <event> indicates needs to happen to <board>
        and do it.

        Return
           - None if <event> was not a board-changing move (that is, if was
             a change in cursor position, or a change in _level made via
            the arrow keys),
           - 1 if <event> was a successful move, and
           - 0 if <event> was an unsuccessful move (for example in the case of
             trying to smash in an invalid location or when the player is not
             allowed further smashes).
        """
        # Get the new "selected" block from the position of the cursor
        block = board.get_selected_block(pygame.mouse.get_pos(), self._level)

        # Remove the highlighting from the old "_selected_block"
        # before highlighting the new one
        if self._selected_block is not None:
            self._selected_block.highlighted = False
        self._selected_block = block
        self._selected_block.highlighted = True

        # Since get_selected_block may have not returned the block at
        # the requested level (due to the level being too low in the tree),
        # set the _level attribute to reflect the level of the block which
        # was actually returned.
        self._level = block.level

        if event.type == pygame.MOUSEBUTTONDOWN:
            block.rotate(event.button)
            return 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if block.parent is not None:
                    self._level -= 1
                return None

            elif event.key == pygame.K_DOWN:
                if len(block.children) != 0:
                    self._level += 1
                return None

            elif event.key == pygame.K_h:
                block.swap(0)
                return 1

            elif event.key == pygame.K_v:
                block.swap(1)
                return 1

            elif event.key == pygame.K_s:
                if self.num_smashes >= self.MAX_SMASHES:
                    print('Can\'t smash again!')
                    return 0
                if block.smash():
                    self.num_smashes += 1
                    return 1
                else:
                    print('Tried to smash at an invalid depth!')
                    return 0

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.

        This method will hold focus until a valid move is performed.
        """
        self._level = 0
        self._selected_block = board

        # Remove all previous events from the queue in case the other players
        # have added events to the queue accidentally.
        pygame.event.clear()

        # Keep checking the moves performed by the player until a valid move
        # has been completed. Draw the board on every loop to draw the
        # selected block properly on screen.
        while True:
            self.renderer.draw(board, self.id)
            # loop through all of the events within the event queue
            # (all pending events from the user input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 1

                result = self.process_event(board, event)
                self.renderer.draw(board, self.id)
                if result is not None and result > 0:
                    # un-highlight the selected block
                    self._selected_block.highlighted = False
                    return 0


class RandomPlayer(Player):
    """A RandomPlayer in the Blocky game.

    A RandomPlayer can randomly use smash limitlessly
    """

    def make_move(self, board: Block) -> int:
        """Randomly choose a move to make on the given board, and apply it,
        mutating the Board as appropriate.

        Return 0 upon successful completion of the move.
        """
        level = random.randint(0, board.max_depth)
        rand_x = random.randint(0, board.size-1)
        rand_y = random.randint(0, board.size-1)
        block = board.get_selected_block((rand_x, rand_y), level)
        block.highlighted = True
        self.renderer.draw(board, self.id)
        pygame.time.wait(TIME_DELAY)
        choice = random.randint(0, 4)
        if choice == 1 or choice == 3:
            block.rotate(choice)
        elif choice == 2:
            block.swap(1)
        elif choice == 0:
            block.swap(0)
        elif choice == 4:
            block.smash()
        block.highlighted = False
        self.renderer.draw(board, self.id)
        return 0


class SmartPlayer(Player):
    """A Randomplayer in the Blocky game.

    A SmartPlayer cannot use smash

    === Public Attributes ===
    num_moves:
        number of random moves the SmartPlayer can assess to determine which
        move will result in highest score
    === Representation Invariants ===
    num_moves >= 5
    """
    num_moves: int

    def __init__(self, renderer: Renderer,
                 player_id: int,
                 goal: Goal, difficulty: int) -> None:
        """Initialize this SmartPlayer with the given <renderer>, <player_id>,
        <goal>, and <difficulty>.

        Set <num_moves> depending on the level of <difficulty>
        """
        Player.__init__(self, renderer, player_id, goal)
        if difficulty == 0:
            self.num_moves = 5
        elif difficulty == 1:
            self.num_moves = 10
        elif difficulty == 2:
            self.num_moves = 25
        elif difficulty == 3:
            self.num_moves = 50
        elif difficulty == 4:
            self.num_moves = 100
        elif difficulty >= 5:
            self.num_moves = 150

    def make_move(self, board: Block) -> int:
        """Assess <num_moves> amount of random moves and apply the move that
        will result in maximum score output, mutating the Board as appropriate.

        Return 0 upon successful completion of the move.
        """
        max_score = 0
        block_to_move = None
        choice = 0
        for _ in range(self.num_moves):
            new_move = self.random_move(board)
            if new_move[1] > max_score:
                max_score = new_move[1]
                block_to_move = new_move[0]
                choice = new_move[2]
        block_to_move.highlighted = True
        self.renderer.draw(board, self.id)
        pygame.time.wait(TIME_DELAY)
        self.random_move(block_to_move, choice)
        block_to_move.highlighted = False
        self.renderer.draw(board, self.id)
        return 0

    def random_move(self, board: Block,
                    choice: Optional[int] = None) -> Tuple[Block, int, int]:
        """Choose a move to make on the given board, apply it
        and record the type of move, the block moved, and the score output.

        if the move is not final Randomly choose the move and reverse it
        after applying it

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.
        """
        score = 0
        final = False
        if choice is None:
            level = random.randint(0, board.max_depth)
            rand_x = random.randint(0, board.size-1)
            rand_y = random.randint(0, board.size-1)
            block = board.get_selected_block((rand_x, rand_y), level)
            choice = random.randint(2, 3)
        else:
            block = board
            final = True
        if choice == 0:
            block.rotate(1)
            score = self.goal.score(board)
            if final is False:
                block.rotate(3)
        elif choice == 1:
            block.rotate(1)
            score = self.goal.score(board)
            if final is False:
                block.rotate(3)
        elif choice == 2:
            block.swap(1)
            score = self.goal.score(board)
            if final is False:
                block.swap(1)
        elif choice == 3:
            block.swap(0)
            score = self.goal.score(board)
            if final is False:
                block.swap(0)
        return block, score, choice


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer',
            'pygame'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
