from constants import BOARD_ROW_LENGTH, BOARD_COL_LENGTH, END_GAME_PLAYER_MESSAGE, BLACK, WHITE
from rulechecker import RuleChecker
from strategy import Strategy
from point import Point
from board import Board

from random import randint
import time
import timeit

class Player():
    def __init__(self, strategy="basic",depth=1,ROW=BOARD_ROW_LENGTH, COL=BOARD_COL_LENGTH):
        self.ROW = ROW
        self.COL = COL
        self.name = None
        self.stone = None
        self.strategy = Strategy(strategy,depth,ROW,COL)
        self.depth = depth

    def register(self):
        self.name = self.strategy.strategy+"Player"+str(hash(time.time()))
        return self.name

    def receive_stones(self, stone):
        self.stone = stone

        self.strategy.stone = stone
        self.strategy.opponent = BLACK if stone == WHITE else WHITE
        return False

    def make_a_move(self, boards):
        return self.strategy.nextmove(boards)

    def end_game(self):
        self.stone, self.opponent = None, None
        return END_GAME_PLAYER_MESSAGE

    def close(self):
        pass