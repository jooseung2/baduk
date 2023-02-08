import unittest
import json
import sys
import os
sys.path.append(os.path.abspath('../src'))

from constants import *
from rulechecker import RuleChecker
from point import Point
from board import Board

rc = RuleChecker(5,5)

class Test(unittest.TestCase):
    def test_GetScores(self):
        ### empty board
        board = \
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        b1 = Board(board,5,5)
        scores = rc.get_scores(b1)
        self.assertEqual(scores[WHITE],scores[BLACK],0)

    def test_GetScores_emptyterritory(self):
        ### count empty territories
        board = \
        [["B", " ", " ", " ", " "],
         [" ", "B", " ", " ", " "], 
         ["B", " ", " ", " ", " "], 
         [" ", " ", " ", "W", " "], 
         [" ", " ", "W", " ", "W"]]
        b1 = Board(board,5,5)
        scores = rc.get_scores(b1)
        self.assertEqual(scores[WHITE],scores[BLACK],4)

    def test_GetScores_noemptyterritory(self):
        ### no empty territories
        board = \
        [["B", " ", " ", " ", " "],
         ["B", "B", " ", " ", " "], 
         ["B", " ", " ", " ", " "], 
         [" ", " ", " ", "W", " "], 
         [" ", " ", "W", "W", "W"]]
        b1 = Board(board,5,5)
        scores = rc.get_scores(b1)
        self.assertEqual(scores[WHITE],scores[BLACK],4)

    def test_GetScores_twoemptyterritories(self):
        ### 
        board = \
        [[" ", "B", " ", "W", " "],
         [" ", "B", " ", "W", " "], 
         [" ", "B", " ", "W", " "], 
         [" ", "B", " ", "W", " "], 
         [" ", "B", " ", "W", " "]]
        b1 = Board(board,5,5)
        scores = rc.get_scores(b1)
        self.assertEqual(scores[WHITE],scores[BLACK],10)

        ### 
        board = \
        [["W", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        b1 = Board(board,5,5)
        scores = rc.get_scores(b1)
        self.assertEqual(scores[WHITE],25)
        self.assertEqual(scores[BLACK],0)

    def test_GetAddedStones(self):

        # base case #1 : no added stone
        next_board = \
        [["W", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        prev_board = \
        [["W", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        nb, pb = Board(next_board,5,5), Board(prev_board,5,5)

        self.assertCountEqual(rc._get_added_stones(nb, pb),[])

    def test_GetAddedStones_oneaddedstone(self):
        # base case #2: one added stone
        next_board = \
        [["W", "B", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        prev_board = \
        [["W", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        nb, pb = Board(next_board,5,5), Board(prev_board,5,5)

        self.assertCountEqual(rc._get_added_stones(nb, pb),\
            [{"stone":BLACK, "point":Point(0,1)}])

    def test_GetAddedStones_multipleaddedstones(self):
        # multiple added stones
        next_board = \
        [["W", "B", "W", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        prev_board = \
        [["W", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        nb, pb = Board(next_board,5,5), Board(prev_board,5,5)

        self.assertCountEqual(rc._get_added_stones(nb, pb),\
            [{"stone":BLACK, "point":Point(0,1)},
            {"stone":WHITE, "point":Point(0,2)}])

    def test_GetAddedStones_ignoremissingstones(self):
        # do not consider missing stones
        next_board = \
        [["W", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        prev_board = \
        [["W", "B", "W", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]

        nb, pb = Board(next_board,5,5), Board(prev_board,5,5)
        self.assertCountEqual(rc._get_added_stones(nb, pb),[])

    def test_getBoardAfterAddingStone(self):
        ### base case
        board = \
        [[" ", "B", " ", "W", " "],
         [" ", "B", " ", "W", " "], 
         [" ", "B", " ", "W", " "], 
         [" ", "B", " ", "W", " "], 
         [" ", "B", " ", "W", " "]]
        b1 = Board(board,5,5)
        stone = BLACK
        point = Point(0,0)

        result = \
        [["B", "B", " ", "W", " "],
         [" ", "B", " ", "W", " "], 
         [" ", "B", " ", "W", " "], 
         [" ", "B", " ", "W", " "], 
         [" ", "B", " ", "W", " "]]
        r1 = Board(result,5,5)
        self_capture = False

        self.assertEqual(rc.get_board_after_adding_stone(b1,stone,point),\
            (r1,self_capture))

    def test_getBoardAfterAddingStone_captureenemy(self):
        ### capture enemy
        board = \
        [["W", " ", " ", " ", " "],
         ["B", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        b1 = Board(board,5,5)
        stone = BLACK
        point = Point(0,1)

        result = \
        [[" ", "B", " ", " ", " "],
         ["B", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        r1 = Board(result,5,5)
        self_capture = False

        self.assertEqual(rc.get_board_after_adding_stone(b1,stone,point),\
            (r1,self_capture))

    def test_getBoardAfterAddingStone_captureandnosuicide(self):
        ### capture enemy to avoid self-capture
        board = \
        [[" ", " ", " ", " ", " "],
         [" ", "W", "B", " ", " "], 
         ["W", "B", " ", "B", " "], 
         [" ", "W", "B", " ", " "], 
         [" ", " ", " ", " ", " "]]
        b1 = Board(board,5,5)
        stone = WHITE
        point = Point(2,2)

        result = \
        [[" ", " ", " ", " ", " "],
         [" ", "W", "B", " ", " "], 
         ["W", " ", "W", "B", " "], 
         [" ", "W", "B", " ", " "], 
         [" ", " ", " ", " ", " "]]
        r1 = Board(result,5,5)
        self_capture = False

        self.assertEqual(rc.get_board_after_adding_stone(b1,stone,point),\
            (r1,self_capture))

        board = \
        [["W","W","B","W"," "],
         ["W","W","B","W","W"], 
         [" ","W","B","W","W"], 
         ["B","W","B","W","W"], 
         ["B","W","B","W","W"]]
        b1 = Board(board,5,5)
        stone = BLACK
        point = Point.from_str("1-3")

        result = \
        [[" "," ","B","W"," "],
         [" "," ","B","W","W"], 
         ["B"," ","B","W","W"], 
         ["B"," ","B","W","W"], 
         ["B"," ","B","W","W"]]
        r1 = Board(result,5,5)
        self_capture = False

        self.assertEqual(rc.get_board_after_adding_stone(b1,stone,point),\
            (r1,self_capture))

    def test_getBoardAfterAddingStone_catchsuicide(self):
        ### self-capture
        board = \
        [[" ", "W", "B", " ", " "],
         ["W", "B", " ", " ", " "], 
         ["B", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        b1 = Board(board,5,5)
        stone = WHITE
        point = Point(0,0)

        _, sc = rc.get_board_after_adding_stone(b1,stone,point)
        self.assertTrue(sc)

    def test_getStonesWithNoLiberty(self):
        ### base case: has liberty
        board = \
        [[" ", "W", "B", " ", " "],
         ["W", "B", " ", " ", " "], 
         ["B", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        b1 = Board(board,5,5)
        result = rc._get_stones_with_no_liberty(b1)
        answer = []
        self.assertCountEqual(result, answer)

    def test_getStonesWithNoLiberty_noliberty(self):
        ### no liberties
        board = \
        [["W", "B", " ", " ", " "],
         ["B", " ", " ", " ", " "], 
         [" ", " ", "W", "W", "W"], 
         [" ", " ", "W", "B", "B"], 
         [" ", " ", "W", "W", "W"]]
        b1 = Board(board,5,5)
        result = rc._get_stones_with_no_liberty(b1)
        answer = [(WHITE, Point(0,0)), (BLACK, Point(3,4)), (BLACK, Point(3,3))]
        self.assertCountEqual(result, answer)

    def test_CheckLegality(self):
        # invalid history 1: 2 consecutive passes
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
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        ]
        boards = [Board(i,5,5) for i in boards]
        stone = BLACK
        point = Point(1,2)

        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_incorrectSecondTurn(self):
        # invalid history 2: black had the second turn
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
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        ]
        boards = [Board(i,5,5) for i in boards]
        stone = BLACK
        point = Point.from_str("1-2")
        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_incorrectSecondTurnAndNotWhiteTurn(self):
        # invalid history 3: black had the second turn & not white's turn
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
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        ]
        boards = [Board(i,5,5) for i in boards]
        stone = WHITE
        point = Point.from_str("1-2")
        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])
    
    def test_CheckLegality_notWhiteTurn(self):
        # invalid history 4: not white's turn
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
        boards = [Board(i,5,5) for i in boards]
        stone = WHITE
        point = Point.from_str("1-2")
        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_BlackPassBlack(self):
        # valid history 1: black-pass-black
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
        boards = [Board(i,5,5) for i in boards]
        stone = BLACK
        point = Point.from_str("1-2")
        self.assertTrue(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_AlreadyAStone(self):
        # invalid history 5: already a stone there
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
        boards = [Board(i,5,5) for i in boards]
        stone = BLACK
        point = Point.from_str("3-4")
        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_notBlackTurn(self):
        # invalid history 5: not a black turn
        boards = \
        [
        [["B", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "W", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "W", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        ]
        boards = [Board(i,5,5) for i in boards]
        stone = BLACK
        point = Point.from_str("1-4")
        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_WhiteBlackWhite(self):
        # valid history 2: white-black-white
        boards = \
        [
        [["B", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "W", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "W", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        ]
        boards = [Board(i,5,5) for i in boards]
        stone = WHITE
        point = Point.from_str("1-4")
        self.assertTrue(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_twoConsecutiveWhiteTurns(self):
        # invalid history 6: white had 2 consecutive turns
        boards = \
        [
        [["W", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "W", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", "W", " ", " "], 
         [" ", " ", " ", " ", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "]]
        ]
        boards = [Board(i,5,5) for i in boards]
        stone = WHITE
        point = Point.from_str("1-4")
        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_koRule1(self):
        # invalid history 7: ko rule
        boards = \
        [
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", "W", "B"], 
         [" ", " ", "W", " ", "W"]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", "W", "B"], 
         [" ", " ", "W", "B", " "]],
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", " ", " "], 
         [" ", " ", " ", "W", "B"], 
         [" ", " ", "W", "B", " "]]
        ]
        boards = [Board(i,5,5) for i in boards]
        stone = BLACK
        point = Point.from_str("4-5")
        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_koRule2(self):
        # invalid history 8: ko rule
        boards = \
        [
        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", "B", "B", "B", "B"], 
         [" ", " ", " ", "W", "B"], 
         [" ", "B", "W", " ", "W"]],

        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", "B", "B", "B", "B"], 
         [" ", " ", " ", "W", "B"], 
         [" ", "B", "W", "B", " "]],

        [[" ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " "], 
         [" ", "B", "B", "B", "B"], 
         [" ", " ", " ", "W", "B"], 
         [" ", "B", "W", " ", "W"]]
        ]
        boards = [Board(i,5,5) for i in boards]
        stone = BLACK
        point = Point.from_str("5-1")
        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_koRule3(self):
        # invalid history 9: ko rule
        boards = \
        [
        [["W","B","B"," ","B"],
         ["W","B","B","W","W"], 
         ["W","B"," ","B","W"], 
         ["W","W","B","W","W"], 
         ["W","W","B","B","W"]],

        [["W","B","B"," ","B"],
         ["W","B","B","W","W"], 
         ["W","B","W"," ","W"], 
         ["W","W","B","W","W"], 
         ["W","W","B","B","W"]],

        [["W","B","B"," ","B"],
         ["W","B","B","W","W"], 
         ["W","B"," "," ","W"], 
         ["W","W","B","W","W"], 
         ["W","W","B","B","W"]]
        ]
        boards = [Board(i,5,5) for i in boards]
        stone = WHITE
        point = Point.from_str("3-3")
        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_capture(self):
        # valid history 3: capture 
        # test5, 4th last one (prof's)
        boards = \
        [
        [["W","W","B"," "," "],
         ["W","W","B","W","W"], 
         [" ","W","B","W","W"], 
         ["B","W","B","W","W"], 
         ["B","W","B","W","W"]],

        [["W","W","B"," "," "],
         ["W","W","B","W","W"], 
         [" "," ","B","W","W"], 
         ["B","W","B","W","W"], 
         ["B","W","B","W","W"]],

        [["W","W","B"," "," "],
         ["W","W","B","W","W"], 
         [" "," "," ","W","W"], 
         ["B","W","B","W","W"], 
         ["B","W","B","W","W"]]
        ]
        boards = [Board(i,5,5) for i in boards]
        stone = BLACK
        point = Point.from_str("1-3")
        self.assertTrue(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_selfcapture1(self):
        # invalid history 10: self-capture 
        # test5, 5th last one (prof's)
        boards = \
        [
        [["W","W","B","W"," "],
         ["W","W","W","W","W"], 
         [" ","W","B","W","W"], 
         ["B","W","B","W","W"], 
         ["B","W","B","W","W"]],

        [["W","W","B","W"," "],
         ["W","W","W","W","W"], 
         [" "," ","B","W","W"], 
         ["B","W","B","W","W"], 
         ["B","W","B","W","W"]],

        [["W","W","B","W"," "],
         ["W","W","W","W","W"], 
         [" "," "," ","W","W"], 
         ["B","W","B","W","W"], 
         ["B","W","B","W","W"]]
        ]
        boards = [Board(i,5,5) for i in boards]
        stone = BLACK
        point = Point.from_str("1-3")
        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_selfcapture2(self):
        # invalid history 10: self-capture 
        # test5, 5th last one (prof's)
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
        boards = [Board(i,9,9) for i in boards]
        stone = BLACK
        point = Point.from_str("6-4")
        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_captureThenMoveOn(self):
        boards = \
        [
        [[" "," ","B"," ","B"],
         [" ","B","B","B","W"], 
         [" ","B"," ","B","W"], 
         [" ","B","B","W","W"], 
         [" "," ","B","B"," "]],

        [[" "," ","B"," ","B"],
         [" ","B"," ","B","W"], 
         [" ","B","W","B","W"], 
         [" ","B","B","W","W"], 
         [" "," ","B","B"," "]],

        [[" "," ","B"," ","B"],
         [" ","B"," ","B","W"], 
         [" ","B"," ","B","W"], 
         [" ","B","B","W","W"], 
         [" "," ","B","B"," "]]
        ]

        boards = [Board(i,5,5) for i in boards]
        stone = WHITE
        point = Point.from_str("1-1")
        self.assertTrue(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_didNotClearStoneWithoutLiberty(self):
        boards = \
        [
        [[" "," ","B"," ","B"],
         [" ","B","B","B","W"], 
         [" ","B","W","B","W"], 
         [" ","B","B","W","W"], 
         [" "," ","B","B"," "]],

        [[" "," ","B"," ","B"],
         [" ","B"," ","B","W"], 
         [" ","B","W","B","W"], 
         [" ","B","B","W","W"], 
         [" "," ","B","B"," "]],

        [[" "," ","B"," ","B"],
         [" ","B"," ","B","W"], 
         [" ","B"," ","B","W"], 
         [" ","B","B","W","W"], 
         [" "," ","B","B"," "]]
        ]

        boards = [Board(i,5,5) for i in boards]
        stone = WHITE
        point = Point.from_str("1-1")
        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_twoConsecutivePasses_Black(self):
        boards = \
        [
        [[" "," ","B"," ","B"],
         [" ","B"," ","B","W"], 
         [" ","B"," ","B","W"], 
         [" ","B","B","W","W"], 
         [" "," ","B","B"," "]],

        [[" "," ","B"," ","B"],
         [" ","B"," ","B","W"], 
         [" ","B"," ","B","W"], 
         [" ","B","B","W","W"], 
         [" "," ","B","B"," "]],

        [[" "," ","B"," ","B"],
         [" ","B"," ","B","W"], 
         [" ","B"," ","B","W"], 
         [" ","B","B","W","W"], 
         [" "," ","B","B"," "]]
        ]

        boards = [Board(i,5,5) for i in boards]
        stone = BLACK
        point = Point.from_str("1-1")
        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])

    def test_CheckLegality_twoConsecutivePasses_White(self):
        boards = \
        [
        [[" "," ","B"," ","B"],
         [" ","B"," ","B","W"], 
         [" ","B"," ","B","W"], 
         [" ","B","B","W","W"], 
         [" "," ","B","B"," "]],

        [[" "," ","B"," ","B"],
         [" ","B"," ","B","W"], 
         [" ","B"," ","B","W"], 
         [" ","B","B","W","W"], 
         [" "," ","B","B"," "]],

        [[" "," ","B"," ","B"],
         [" ","B"," ","B","W"], 
         [" ","B"," ","B","W"], 
         [" ","B","B","W","W"], 
         [" "," ","B","B"," "]]
        ]

        boards = [Board(i,5,5) for i in boards]
        stone = WHITE
        point = Point.from_str("1-1")
        self.assertFalse(rc.check_legality(stone, point, boards)["legal"])
if __name__ == "__main__":
    unittest.main()
