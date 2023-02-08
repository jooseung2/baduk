import unittest
import sys
import os
sys.path.append(os.path.abspath('../src'))

from constants import *
from board import Board
from player import Player

class Test(unittest.TestCase):
    def test_makeamove_shouldpass(self):
        p1 = Player(strategy='basic',ROW=5,COL=5)
        p1.receive_stones(WHITE)
        boards = \
        [
        [["W", "W", "W", "W", "W"],
         ["W", "W", "W", "W", "W"], 
         ["W", "W", "W", "W", "W"], 
         ["W", "W", "W", "W", "W"], 
         ["W", "W", "W", "W", " "]],
        [["W", "W", "W", "W", "W"],
         ["W", "W", "W", "W", "W"], 
         ["W", "W", "W", "W", "W"], 
         ["W", "W", "W", "W", "W"], 
         ["W", "W", "W", "W", " "]],
        [["W", "W", "W", "W", "W"],
         ["W", "W", "W", "W", "W"], 
         ["W", "W", "W", "W", "W"], 
         ["W", "W", "W", "W", " "], 
         ["W", "W", "W", "W", " "]]
        ]
        boards = [Board(i,5,5) for i in boards]
        self.assertEqual(p1.make_a_move(boards), PASS)
    
    def test_makeamove_checkindex(self):
        p1 = Player(strategy='basic',ROW=5,COL=5)
        p1.receive_stones(WHITE)
        boards = \
        [
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        ]
        boards = [Board(i,5,5) for i in boards]
        self.assertEqual(p1.make_a_move(boards), "1-1")
    
    def test_makeamove_should_return_right_index(self):
        p1 = Player(strategy='basic',ROW=5,COL=5)
        p1.receive_stones(WHITE)

        boards = \
        [
        [["W", "W", "W", "B", " "],
         ["W", "W", "W", "B", " "], 
         ["W", "W", "W", "B", " "], 
         [" ", "W", "W", "B", "B"], 
         ["B", "B", "W", "B", " "]],
        [["W", "W", "W", "B", "W"],
         ["W", "W", "W", "B", "W"], 
         ["W", "W", "W", "B", "W"], 
         [" ", "W", "W", "B", " "], 
         ["B", "B", "W", "B", " "]],
        [["W", "W", "W", "B", "W"],
         ["W", "W", "W", "B", "W"], 
         ["W", "W", "W", "B", " "], 
         [" ", "W", "W", "B", " "], 
         ["B", "B", "W", "B", " "]]
        ]
        boards = [Board(i,5,5) for i in boards]
        self.assertEqual(p1.make_a_move(boards), "1-4")
if __name__ == "__main__":
    unittest.main()