import unittest
import sys
import os
sys.path.append(os.path.abspath('../src'))

from constants import *
from point import Point
from board import Board

class Test(unittest.TestCase):
    def test_validateboard_invalidStone(self):
        board = \
        [["W", "B", " ", " ", " "],
         ["B", " ", " ", " ", " "], 
         [" ", " ", "C", "W", "W"], 
         [" ", " ", "W", "B", "B"], 
         [" ", " ", "W", "W", "W"]]
        b1 = Board(board,5,5)
        self.assertFalse(Board.validate_board(b1))

    def test_validateboard_deadStones(self):
        board = \
        [["W", "B", " ", " ", " "],
         ["B", " ", " ", " ", " "], 
         [" ", " ", "W", "W", "W"], 
         [" ", " ", "W", "B", "B"],
         [" ", " ", "W", "B", "B"], 
         [" ", " ", "W", "W", "W"]]
        b2 = Board(board,5,5)
        self.assertFalse(Board.validate_board(b2))
        board = \
        [["W", "B", " ", " ", " "],
         ["B", " ", " ", " ", " "], 
         [" ", " ", " ", "W", "W"], 
         [" ", " ", "W", "B", "B"], 
         [" ", " ", "W", "W", "W"]]
        b3 = Board(board,5,5)
        self.assertFalse(Board.validate_board(b3))

    def test_isempty(self):
        board = \
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        b1 = Board(board,5,5)
        self.assertTrue(b1.is_empty())
        b1.place(BLACK,Point(1,2))
        self.assertFalse(b1.is_empty())

    def test_copy(self):
        board = \
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        b1 = Board(board,5,5)
        b2 = b1
        b_copy = b1.copy()
        b1.place(BLACK,Point(1,2))
        self.assertFalse(b1 == b_copy)
        self.assertTrue(b1 == b2)

    def test_isoccupied(self):
        board = \
        [[" ", "B", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        b1 = Board(board,5,5)
        self.assertTrue(b1.is_occupied(Point(0,1)))

    def test_occupies(self):
        board = \
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", "B", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        b1 = Board(board,5,5)
        self.assertTrue(b1.occupies(BLACK, Point(2,1)))

    def test_isreachable(self):
        board = \
        [["B", "B", "W", " ", " "],
         ["W", "B", "W", " ", " "], 
         ["W", "B", "W", " ", " "], 
         ["W", "B", "W", "W", " "], 
         ["W", "B", "B", "B", "B"]]
        b1 = Board(board,5,5)
        self.assertTrue(b1.is_reachable(Point(0,0),EMPTY))
        self.assertTrue(b1.is_reachable(Point(0,4),WHITE))
        self.assertFalse(b1.is_reachable(Point(4,0),EMPTY))

    def test_place(self):
        board = \
        [["B", "B", "W", " ", " "],
         ["W", "B", "W", " ", " "], 
         ["W", "B", "W", " ", " "], 
         ["W", "B", "W", "W", " "], 
         ["W", "B", "B", "B", "B"]]
        b1 = Board(board,5,5)
        self.assertEqual(CANNOT_PLACE_MESSAGE, b1.place(BLACK, Point(2,2)))
        b1.place(BLACK,Point(0,4))
        self.assertTrue(b1.occupies(BLACK,Point(0,4)))

    def test_remove(self):
        board = \
        [["B", "B", "W", " ", " "],
         ["W", "B", "W", " ", " "], 
         ["W", "B", "W", " ", " "], 
         ["W", "B", "W", "W", " "], 
         ["W", "B", "B", "B", "B"]]
        b1 = Board(board,5,5)
        self.assertEqual(CANNOT_REMOVE_MESSAGE, b1.remove(BLACK, Point(2,2)))
        self.assertEqual(CANNOT_REMOVE_MESSAGE, b1.remove(BLACK, Point(2,3)))
        b1.remove(WHITE, Point(2,2))
        self.assertFalse(b1.is_occupied(Point(2,2)))

    def get_points(self):
        board = \
        [["B", "B", "W", " ", " "],
         ["W", "B", "W", " ", " "], 
         ["W", "B", "W", " ", " "], 
         ["W", "B", "W", "W", " "], 
         ["W", "B", "B", "B", "B"]]
        b1 = Board(board,5,5)
        self.assertEqual(b1.get_points(BLACK),9)
        self.assertEqual(b1.get_points(WHITE),9)
        self.assertEqual(b1.get_points(EMPTY),7)

    def test_get_chains_and_liberties(self):
        board = \
        [["W", "B", " ", " ", " "],
         ["B", " ", " ", " ", " "], 
         [" ", " ", "W", "W", "W"], 
         [" ", " ", "W", "B", "B"], 
         [" ", " ", "W", "W", "W"]]
        b1 = Board(board,5,5)

        answer = [
            {"chain_color" : WHITE,
            "chain" : [(WHITE, Point(0,0))],
            "liberties" : []},

            {"chain_color" : BLACK,
            "chain" : [(BLACK, Point(0,1))],
            "liberties" : sorted([Point(0,2), Point(1,1)])},

            {"chain_color" : BLACK,
            "chain" : [(BLACK, Point(1,0))],
            "liberties" : sorted([Point(1,1), Point(2,0)])},

            {"chain_color" : BLACK,
            "chain" : [(BLACK, Point(3,3)), (BLACK, Point(3,4))],
            "liberties" : []},

            {"chain_color" : WHITE,
            "chain" : sorted([(WHITE, Point(2,2)),(WHITE, Point(3,2)),(WHITE, Point(4,2)),
                (WHITE, Point(2,3)),(WHITE, Point(2,4)),(WHITE, Point(4,3)),(WHITE, Point(4,4))]),
            "liberties" : sorted([Point(2,1), Point(3,1), Point(4,1), Point(1,2), Point(1,3), Point(1,4)])},
        ]
        self.assertCountEqual(b1.get_chains_and_their_liberties(), answer)

    def test_is_reachable(self):
        board =\
        [["B", " ", " ", " ", " "],
         [" ", "W", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        
        b1 = Board(board,5,5)
        self.assertTrue(b1.is_reachable(Point(1,0), BLACK))

if __name__ == "__main__":
    unittest.main()
