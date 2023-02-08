import unittest
import json
import sys
import os
sys.path.append(os.path.abspath('../src'))

from player import Player
from rulechecker import RuleChecker
from referee import GameState
import referee
from point import Point
from board import Board
from constants import WHITE, BLACK

class Test(unittest.TestCase):
    def test_executeaction_easycase(self):
        self.maxDiff = None
        gs = GameState(5,5)
        gs.players = {BLACK:{"name":"black_p","player":Player()},
                    WHITE:{"name":"white_p","player":Player()}}
        referee.execute_action(Point(3,3),gs)

        history = \
        [Board(i,5,5) for i in
        [
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", "B", " "], 
         [" ", " ", " ", " ", " "]],
         
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        ]
        ]
        self.assertEqual(gs.history, history)

    def test_executeaction_illegalaction(self):
        gs = GameState(5,5)
        gs.players = {BLACK:{"name":"black_p","player":Player()},
                    WHITE:{"name":"white_p","player":Player()}}
        gs.history = \
        [Board(i,5,5) for i in 
        [
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "W", " ", " "], 
         [" ", " ", "B", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "B", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        ]
        ]
        try:
            referee.execute_action(Point(3,2),gs)
            self.assertFalse(True) # should not get here
        except ValueError:
            self.assertTrue(True)

    def test_handlepass_wasnotpass(self):
        gs = GameState(5,5)
        gs.players = {BLACK:{"name":"black_p","player":Player()},
                    WHITE:{"name":"white_p","player":Player()}}
        gs.history = \
        [Board(i,5,5) for i in 
        [
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "W", " ", " "], 
         [" ", " ", "B", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "B", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        ]
        ]

        history = \
        [Board(i,5,5) for i in 
        [
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "W", " ", " "], 
         [" ", " ", "B", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "W", " ", " "], 
         [" ", " ", "B", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "B", " ", " "]]
        ]
        ]

        referee.handle_pass(gs)
        self.assertTrue(gs.is_pass)
        self.assertEqual(gs.current_stone, WHITE)
        self.assertEqual(gs.history, history)
        
    def test_handlepass_waspass(self):
        gs = GameState(5,5)
        gs.players = {BLACK:{"name":"black_p","player":Player()},
                    WHITE:{"name":"white_p","player":Player()}}
        gs.current_stone = WHITE
        gs.is_pass = True
        gs.history = \
        [Board(i,5,5) for i in 
        [
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "W", " ", " "], 
         [" ", " ", "B", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "W", " ", " "], 
         [" ", " ", "B", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "B", " ", " "]]
        ]
        ]

        referee.handle_pass(gs)
        self.assertTrue(gs.game_over)
        self.assertFalse(gs.cheated)
        self.winner = ["black_p","white_p"]
        
    def test_handlecheater(self):
        gs = GameState(5,5)
        gs.players = {BLACK:{"name":"black_p","player":Player()},
                    WHITE:{"name":"white_p","player":Player()}}
        gs.current_stone = WHITE
        gs.is_pass = True
        gs.history = \
        [Board(i,5,5) for i in 
        [
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "W", " ", " "], 
         [" ", " ", "B", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "W", " ", " "], 
         [" ", " ", "B", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "B", " ", " "]]
        ]
        ]

        referee.handle_cheater(gs)

        self.assertTrue(gs.game_over)
        self.assertTrue(gs.cheated)
        self.assertEqual(gs.winner, ["black_p"])
        
if __name__ == "__main__":
    unittest.main()
