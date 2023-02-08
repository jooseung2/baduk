import unittest
import sys
import os
sys.path.append(os.path.abspath('../src'))

from point import Point
from board import Board
from player import Player
from constants import *
from strategy import Strategy

class Test(unittest.TestCase):
    def test_h1(self):
        pass        

    def test_checkLegalityNextMove(self):
        boards = \
        [
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "B", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "B", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        ]
        abstrat = Strategy("alphabeta", 2, 5, 5)
        boards = [Board(i,5,5) for i in boards]
        point = Point(1,3)
        stone = BLACK
        result = abstrat.checkLegalityNextMove(boards, point, stone)
        self.assertTrue(result["legal"])
    
    def test_getLegalMoves(self):
        boards = \
        [
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "B", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "B", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        ]
        abstrat = Strategy("alphabeta", 2, 5, 5)
        boards = [Board(i,5,5) for i in boards]
        stone = BLACK
        legalmoves = abstrat.getLegalMoves(boards, stone)
        points = [i[0] for i in legalmoves]
        results = [i[1] for i in legalmoves]

        points_answer = []
        results_answer = []
        for i in range(5):
            for j in range(5):
                if (i,j) != (3,2):
                    points_answer.append(Point(i,j))
                    results_answer.append({"legal":True,"new_board":boards[0].copy().place(stone,Point(i,j))})

        self.assertCountEqual(points, points_answer)
        self.assertCountEqual(results, results_answer)

    def test_makeamove1(self):
        boards = \
        [
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "B", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "B", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        ]
        p1 = Player("alphabeta", 2, 5, 5)
        boards = [Board(i,5,5) for i in boards]
        p1.receive_stones(BLACK)
        p1.make_a_move(boards)

    def test_makeamove2_passtofinish(self):
        boards = \
        [
        [["B", "B", "B", "B", " ", "B", " ", "B", " "],
        [" ", "B", "B", "B", "B", "B", "B", " ", "B"],
        ["B", "B", " ", "B", " ", "B", "B", "B", " "],
        ["B", "B", "B", "B", "B", "B", " ", " ", "B"],
        ["W", "B", "W", "B", "B", " ", " ", "B", "B"],
        ["W", "W", "W", "B", " ", " ", " ", " ", " "],
        ["W", "W", "W", " ", "B", " ", " ", " ", "B"],
        ["W", "W", "W", "B", "B", "B", "B", "B", " "],
        ["W", "W", "B", " ", " ", " ", " ", "B", " "]],

        [["B", "B", "B", "B", " ", "B", " ", "B", " "],
        [" ", "B", "B", "B", "B", "B", "B", " ", "B"],
        ["B", "B", " ", "B", " ", "B", "B", "B", " "],
        ["B", "B", "B", "B", "B", "B", " ", " ", "B"],
        ["W", "B", "W", "B", "B", " ", " ", "B", "B"],
        ["W", "W", "W", "B", " ", " ", " ", " ", " "],
        ["W", "W", "W", " ", "B", " ", " ", " ", "B"],
        ["W", "W", "W", "B", "B", "B", "B", "B", " "],
        ["W", "W", "B", " ", " ", " ", " ", "B", " "]],

        [["B", "B", "B", "B", " ", "B", " ", "B", " "],
        [" ", "B", "B", "B", "B", "B", "B", " ", "B"],
        ["B", "B", " ", "B", " ", "B", "B", "B", " "],
        ["B", "B", "B", "B", "B", "B", " ", " ", "B"],
        ["W", "B", "W", "B", "B", " ", " ", "B", "B"],
        ["W", "W", "W", "B", " ", " ", " ", " ", " "],
        ["W", "W", "W", " ", "B", " ", " ", " ", "B"],
        ["W", "W", " ", "B", "B", "B", "B", "B", " "],
        ["W", "W", "B", " ", " ", " ", " ", "B", " "]]
        ]
        p1 = Player("alphabeta",2,9,9)
        boards = [Board(i,9,9) for i in boards]
        p1.receive_stones(BLACK)
        self.assertEqual(p1.make_a_move(boards), PASS)

    def test_makeamove_multiprocessing1(self):
        # a process has no point to search
        p1 = Player("alphabeta",2,9,9)
        p1.receive_stones(BLACK)
        boards = \
        [
        [[BLACK, EMPTY, WHITE, BLACK, BLACK, WHITE, EMPTY, WHITE, BLACK],
        [BLACK, EMPTY, WHITE, WHITE, BLACK, WHITE, WHITE, WHITE, EMPTY],
        [WHITE, WHITE, EMPTY, WHITE, BLACK, BLACK, WHITE, WHITE, EMPTY],
        [WHITE, WHITE, WHITE, WHITE, BLACK, BLACK, BLACK, WHITE, WHITE],
        [WHITE, BLACK, EMPTY, WHITE, BLACK, BLACK, WHITE, WHITE, EMPTY],
        [BLACK, WHITE, WHITE, EMPTY, WHITE, EMPTY, WHITE, BLACK, EMPTY],
        [BLACK, WHITE, WHITE, WHITE, EMPTY, WHITE, WHITE, WHITE, WHITE],
        [BLACK, WHITE, EMPTY, WHITE, WHITE, EMPTY, WHITE, EMPTY, WHITE],
        [EMPTY, BLACK, WHITE, EMPTY, BLACK, WHITE, EMPTY, WHITE, EMPTY]],

        [[BLACK, EMPTY, WHITE, BLACK, BLACK, WHITE, EMPTY, WHITE, BLACK],
        [BLACK, EMPTY, WHITE, WHITE, BLACK, WHITE, WHITE, WHITE, EMPTY],
        [WHITE, WHITE, EMPTY, WHITE, BLACK, BLACK, WHITE, WHITE, EMPTY],
        [EMPTY, WHITE, WHITE, WHITE, BLACK, BLACK, BLACK, WHITE, WHITE],
        [WHITE, BLACK, EMPTY, WHITE, BLACK, BLACK, WHITE, WHITE, EMPTY],
        [BLACK, WHITE, WHITE, EMPTY, WHITE, EMPTY, WHITE, BLACK, EMPTY],
        [BLACK, WHITE, WHITE, WHITE, EMPTY, WHITE, WHITE, WHITE, WHITE],
        [BLACK, WHITE, EMPTY, WHITE, WHITE, EMPTY, WHITE, EMPTY, WHITE],
        [EMPTY, BLACK, WHITE, EMPTY, BLACK, WHITE, EMPTY, WHITE, EMPTY]],

        [[BLACK, EMPTY, WHITE, BLACK, BLACK, WHITE, EMPTY, WHITE, BLACK],
        [BLACK, EMPTY, WHITE, WHITE, BLACK, WHITE, WHITE, WHITE, EMPTY],
        [WHITE, WHITE, EMPTY, WHITE, BLACK, BLACK, WHITE, WHITE, EMPTY],
        [EMPTY, WHITE, WHITE, WHITE, BLACK, BLACK, BLACK, WHITE, WHITE],
        [WHITE, BLACK, EMPTY, WHITE, BLACK, BLACK, WHITE, WHITE, EMPTY],
        [EMPTY, WHITE, WHITE, EMPTY, WHITE, EMPTY, WHITE, BLACK, EMPTY],
        [BLACK, WHITE, WHITE, WHITE, EMPTY, WHITE, WHITE, WHITE, WHITE],
        [BLACK, WHITE, EMPTY, WHITE, WHITE, EMPTY, WHITE, EMPTY, WHITE],
        [EMPTY, BLACK, WHITE, EMPTY, BLACK, WHITE, EMPTY, WHITE, EMPTY]]
        ]
        boards = [Board(i) for i in boards]

        self.assertEqual(p1.make_a_move(boards),"2-1")

    def test_makeamove_multiprocessing_crash(self):
        p1 = Player("alphabeta",2,9,9)
        p1.receive_stones(BLACK)
        boards = \
        [
        [[EMPTY, WHITE, EMPTY, WHITE, WHITE, EMPTY, WHITE, WHITE, EMPTY],
        [WHITE, EMPTY, WHITE, WHITE, BLACK, WHITE, WHITE, EMPTY, WHITE],
        [EMPTY, WHITE, EMPTY, WHITE, EMPTY, WHITE, EMPTY, WHITE, EMPTY],
        [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, EMPTY, WHITE],
        [WHITE, EMPTY, WHITE, WHITE, WHITE, EMPTY, WHITE, WHITE, EMPTY],
        [EMPTY, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE],
        [WHITE, EMPTY, WHITE, EMPTY, WHITE, WHITE, EMPTY, WHITE, EMPTY],
        [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, EMPTY, WHITE],
        [EMPTY, WHITE, EMPTY, WHITE, EMPTY, WHITE, WHITE, WHITE, EMPTY]],

        [[EMPTY, WHITE, BLACK, EMPTY, WHITE, EMPTY, WHITE, WHITE, EMPTY],
        [WHITE, EMPTY, WHITE, WHITE, BLACK, WHITE, WHITE, EMPTY, WHITE],
        [EMPTY, WHITE, EMPTY, WHITE, EMPTY, WHITE, EMPTY, WHITE, EMPTY],
        [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, EMPTY, WHITE],
        [WHITE, EMPTY, WHITE, WHITE, WHITE, EMPTY, WHITE, WHITE, EMPTY],
        [EMPTY, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE],
        [WHITE, EMPTY, WHITE, EMPTY, WHITE, WHITE, EMPTY, WHITE, EMPTY],
        [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, EMPTY, WHITE],
        [EMPTY, WHITE, EMPTY, WHITE, EMPTY, WHITE, WHITE, WHITE, EMPTY]],

        [[EMPTY, WHITE, BLACK, EMPTY, WHITE, EMPTY, WHITE, WHITE, EMPTY],
        [WHITE, EMPTY, WHITE, WHITE, EMPTY, WHITE, WHITE, EMPTY, WHITE],
        [EMPTY, WHITE, EMPTY, WHITE, EMPTY, WHITE, EMPTY, WHITE, EMPTY],
        [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, EMPTY, WHITE],
        [WHITE, EMPTY, WHITE, WHITE, WHITE, EMPTY, WHITE, WHITE, EMPTY],
        [EMPTY, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE],
        [WHITE, EMPTY, WHITE, EMPTY, WHITE, WHITE, EMPTY, WHITE, EMPTY],
        [WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, WHITE, EMPTY, WHITE],
        [EMPTY, WHITE, EMPTY, WHITE, EMPTY, WHITE, WHITE, WHITE, EMPTY]]
        ]
        boards = [Board(i) for i in boards]
        self.assertEqual(p1.make_a_move(boards), PASS)

if __name__ == "__main__":
    unittest.main()