import unittest
import json
import sys
import os
sys.path.append(os.path.abspath('../src'))

from constants import *
from point import Point
from board import Board
from player import Player
from rulechecker import RuleChecker

class Test(unittest.TestCase):
    def test_willsuicide(self):
        p1 = Player("capture",1)
        p1.receive_stones(BLACK)

        boards = \
        [
        [["B", "W", "W", "W", "W", "W", "W", "W", " "],
        ["B", "W", "W", "W", "W", "W", "W", " ", "W"],
        ["B", "B", "B", "W", "W", "W", " ", "W", " "],
        ["B", "B", "B", "W", "W", " ", "W", " ", "W"],
        ["B", "B", "B", "B", "B", "W", " ", "W", " "],
        ["B", "B", "B", "B", "B", "W", "W", " ", "W"],
        ["B", "B", "B", "B", "B", "W", " ", "W", " "],
        ["B", "B", "B", "B", "B", " ", "W", " ", "W"],
        ["B", "B", "B", "B", "B", "W", " ", "W", " "]],

        [["B", "W", "W", "W", "W", "W", "W", "W", " "],
        ["B", "W", "W", "W", "W", "W", "W", " ", "W"],
        ["B", "B", "B", "W", "W", "W", " ", "W", " "],
        ["B", "B", "B", "W", "W", " ", "W", " ", "W"],
        ["B", "B", "B", "B", "B", "W", " ", "W", " "],
        ["B", "B", "B", "B", "B", " ", "W", " ", "W"],
        ["B", "B", "B", "B", "B", "W", " ", "W", " "],
        ["B", "B", "B", "B", "B", " ", "W", " ", "W"],
        ["B", "B", "B", "B", "B", "W", " ", "W", " "]],

        [["B", "W", "W", "W", "W", "W", "W", "W", " "],
        ["B", "W", "W", "W", "W", "W", "W", " ", "W"],
        ["B", "B", "B", "W", "W", "W", " ", "W", " "],
        ["B", "B", "B", "W", "W", " ", "W", " ", "W"],
        ["B", "B", "B", "B", "B", "W", " ", "W", " "],
        ["B", "B", "B", "B", "B", " ", "W", " ", "W"],
        ["B", "B", "B", "B", "B", "W", " ", "W", " "],
        ["B", "B", "B", "B", "B", " ", "W", " ", "W"],
        ["B", "B", "B", "B", " ", "W", " ", "W", " "]]
        ]
        boards = [Board(i) for i in boards]
        self.assertEqual(p1.make_a_move(boards),PASS)

    def test_makeamove_shouldpass(self):
        p1 = Player("capture",1,5, 5)
        p1.receive_stones(BLACK)
        boards = \
        [
        [[" ", "B", "B", "B", "B"],
         ["B", "B", "B", "B", "B"],
         ["B", "B", "B", "B", "B"],
         ["B", "B", "B", "B", "B"],
         ["B", "B", "B", "B", "B"]],
        [[" ", "B", "B", "B", "B"],
         ["B", "B", "B", "B", "B"],
         ["B", "B", "B", "B", "B"],
         ["B", "B", "B", "B", "B"],
         ["B", "B", "B", "B", "B"]],
        [[" ", "B", "B", "B", "B"],
         [" ", "B", "B", "B", "B"],
         ["B", "B", "B", "B", "B"],
         ["B", "B", "B", "B", "B"],
         ["B", "B", "B", "B", "B"]]
        ]
        boards = [Board(i,5,5) for i in boards]
        self.assertEqual(p1.make_a_move(boards), "pass")
    
    def test_stupid_makeamove_normal(self):
        p1 = Player("capture",1,5, 5)
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
    
    def test_capture_makeamove_normal(self):
        p1 = Player("capture",1,5,5)
        p1.receive_stones(WHITE)
        boards = \
        [
        [["B", "W", " ", " ", " "],
         ["B", "W", " ", " ", " "], 
         ["B", "W", " ", " ", " "], 
         ["B", "W", " ", " ", " "], 
         [" ", "W", " ", " ", " "]],
        [["B", "W", " ", " ", " "],
         ["B", "W", " ", " ", " "], 
         ["B", "W", " ", " ", " "], 
         [" ", "W", " ", " ", " "], 
         [" ", "W", " ", " ", " "]],
        [["B", "W", " ", " ", " "],
         ["B", "W", " ", " ", " "], 
         ["B", "W", " ", " ", " "], 
         [" ", "W", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        ]
        boards = [Board(i,5,5) for i in boards]
        self.assertEqual(p1.make_a_move(boards), "1-5")
if __name__ == "__main__":
    unittest.main()