from constants import END_GAME_PLAYER_MESSAGE, GO_CRAZY_MESSAGE, STONES, PASS, TIMEOUT_MAKEAMOVE, TIMEOUT_ENDGAME
from board import Board
from point import Point
from rulechecker import RuleChecker
from exceptions import TimeOutException
from player import Player

import signal

def timeout_handler(signum, frame):
    raise TimeOutException

class PlayerWrapper():
    """
    the snitch player
    """
    def __init__(self, player):
        self.player = player
        self.rc = RuleChecker()
        self.stone = None
        self.name = None

    def register(self):
        if self.name is not None:
            raise ValueError('register] Player has already registered')

        result = self.player.register()
        
        if not isinstance(result, str):
            raise ValueError('register] Incorrect output type: ',result)
        # if result == GO_CRAZY_MESSAGE:
        #     raise ValueError('register] GO has gone crazy!')

        self.name = result
        return result

    def receive_stones(self, stone):
        if self.name is None:
            raise ValueError('receive_stones] Player has not registered yet')
        if self.stone is not None:
            raise ValueError('receive_stones] Player already has stones')

        if stone not in STONES:
            raise ValueError('receive_stones] Received wrong type of stone: ',stone)
        self.player.receive_stones(stone)
        self.stone = stone

    def make_a_move(self, boards):
        if self.name is None:
            raise ValueError('make_a_move] Player has not registered yet')
        if self.stone is None:
            raise ValueError('make_a_move] Player has not received stones yet')

        if not Board.validate_boards(boards):
            raise ValueError('make_a_move] Received defective boards: \n',boards)
        if not self.rc.check_history(self.stone, boards):
            raise ValueError('make_a_move] Board History is not legal: \n',boards)

        # signal.signal(signal.SIGALRM, timeout_handler)
        # signal.alarm(TIMEOUT_MAKEAMOVE)
        # try:
        #     result = self.player.make_a_move(boards)
        # except TimeOutException:
        #     raise ValueError('make_a_move] Player takes too much time to make a move.')
        # else:
        #     signal.alarm(0)

        result = self.player.make_a_move(boards)

        print('{}: {}'.format(self.name, result))
        if result == PASS:
            return result
        else:
            if not Point.validate_point_str(result):
                raise ValueError('make_a_move] Returned with wrong point: ',result)
            if result == GO_CRAZY_MESSAGE:
                raise ValueError('make_a_move] GO has gone crazy!')
            return Point.from_str(result)

    def end_game(self):

        # try:
        #     result = self.player.end_game()
        # except TimeOutException:
        #     raise ValueError('end_game] Player takes too much time to respond.')
        # else:
        #     signal.alarm(0)

        result = self.player.end_game()

        if result == END_GAME_PLAYER_MESSAGE:
            self.stone = None
        return result

    def close(self):
        self.player.close()

class RefereeWrapper():
    def __init__(self, referee):
        self.referee = referee

    def play_a_game(self, players_info):
        if not isinstance(players_info,list):
            raise Exception
        if len(players_info) != 2:
            raise Exception
        for (player, name) in players_info:
            if not isinstance(player, (Player, PlayerWrapper)) or not isinstance(name, str):
                raise Exception

        winner, cheated =  self.referee.play_a_game(players_info)

        if not isinstance(winner, list) or not isinstance(cheated, bool):
            raise Exception
        if len(winner) not in [1,2]:
            raise Exception
        if len(winner) == 2 and cheated:
            raise Exception

        return winner, cheated