import unittest
import io
import contextlib
from unittest.mock import patch
from src.alphabeta import TicTacToe
from src.alphabeta import alpha_beta_value

from tmc import points

from tmc.utils import load, get_stdout


@points('AlphaBeta')
class MainTest(unittest.TestCase):
    def test_empty_board(self):
        self.longMessage = False
        empty_board = 3 * '???'
        state = TicTacToe(empty_board, True)
        self.assertEqual(0, alpha_beta_value(state), msg='Wrong alphabeta value for empty board')

    def test_x_advantage(self):
        self.longMessage = False
        current_board = 'xx?' + 'o??' + 'o??'
        state = TicTacToe(current_board, True)
        self.assertEqual(1, alpha_beta_value(state), msg='Wrong alphabeta value for the board: xx?o??o??')

    def test_o_advantage(self):
        self.longMessage = False
        current_board = 'oo?' + 'x??' + 'x??'
        state = TicTacToe(current_board, False)
        self.assertEqual(-1, alpha_beta_value(state), msg='Wrong alphabeta value for the board: oo?x??x??')
