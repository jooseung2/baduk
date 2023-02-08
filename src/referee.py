import random
import traceback
import json
from time import sleep

from constants import WHITE, BLACK, STONES, PASS, BOARD_ROW_LENGTH, BOARD_COL_LENGTH
from rulechecker import RuleChecker
from board import Board
from exceptions import TimeOutException

class GameState():
    def __init__(self, ROW=BOARD_ROW_LENGTH,COL=BOARD_COL_LENGTH):
        self.current_stone = BLACK
        self.is_pass = False
        self.history = [Board.empty(ROW, COL)]
        self.winner = []
        self.game_over = False
        self.cheated = False
        self.players = {}
        # key is stone color, value is another dict, with keys "name" and "player"
        self.rc = RuleChecker(ROW,COL)

    def switch_player(self):
        self.current_stone = BLACK if self.current_stone == WHITE else WHITE

def _execute_action(point, gs):
    if gs.is_pass:
        gs.is_pass = False

    action_result = gs.rc.check_legality(gs.current_stone, point, gs.history)
    
    if action_result["legal"]:
        new_board = action_result["new_board"]
        gs.history = ([new_board] + gs.history)[:3]
        gs.switch_player()
    else:
        raise ValueError('[referee] Illegal action by player {}'.format(gs.players[gs.current_stone]["name"]))

def _handle_pass(gs):
    if gs.is_pass:
        # consecutive passes
        gs.game_over = True
        _evaluate_winner(gs)
    else:
        # this one passes
        gs.is_pass = True
        gs.switch_player()
        gs.history = ([gs.history[0]] + gs.history)[:3]

def _evaluate_winner(gs):
    """
    calculates score,
    returns list of names of winner(s) in lex.order
    """
    scores = gs.rc.get_scores(gs.history[0])

    gs.game_over = True
    if scores[BLACK] > scores[WHITE]:
        gs.winner = [gs.players[BLACK]["name"]]
    elif scores[BLACK] < scores[WHITE]:
        gs.winner = [gs.players[WHITE]["name"]]
    else:
        gs.winner = sorted([gs.players[WHITE]["name"],gs.players[BLACK]["name"]])

def _handle_cheater(gs):
    gs.game_over = True
    gs.cheated = True
    gs.switch_player()
    winner_color = gs.current_stone
    gs.winner = [gs.players[winner_color]["name"]]

def play_a_game(players_info):
    """
    input: [(p1, p1name), (p2, p2name)]
    output: list of name of the winner, bool indicating if loser cheated
    """
    gs = GameState()
    random.shuffle(players_info)

    # receive-stone
    for index, (player, name) in enumerate(players_info):
        print('[referee: receive-stones] attempt to give {} a stone {}'.format(name, STONES[index]))
        try:
            player.receive_stones(STONES[index])
            gs.players[STONES[index]] = {}
            gs.players[STONES[index]]["name"] = name
            gs.players[STONES[index]]["player"] = player
        except (ValueError, OSError, BrokenPipeError, ConnectionResetError) as e:
            if isinstance(e, (OSError, ConnectionResetError, BrokenPipeError)):
                print('[referee: receive-stones] connection dropped from player')
            else:
                print('referee: {}'.format(e))
            gs.game_over = True
            gs.cheated = True
            # choose other player as the winner
            gs.winner = [players_info[1-index][1]]
            break
        gs.switch_player()

    # make-a-move

    while not gs.game_over:
        print('[referee: make-a-move] ask {} to make a play'.format(gs.players[gs.current_stone]["name"]))
        try:
            action = gs.players[gs.current_stone]["player"].make_a_move(gs.history)
            if isinstance(action, str) and action == PASS:
                _handle_pass(gs)
                print(gs.history[0])
            else:
                _execute_action(action, gs)
                print(gs.history[0])
        except (OSError, ConnectionResetError, BrokenPipeError, ValueError, json.JSONDecodeError, TimeOutException) as e:
            if isinstance(e, (OSError, ConnectionResetError, BrokenPipeError, json.JSONDecodeError)):
                print('[referee: make-a-move] connection dropped from player')
            else:
                print('[referee: {}'.format(e))
            # print(type(e))
            _handle_cheater(gs)

    # end-game
    for player, _ in players_info:
        try:
            player.end_game()
        except (OSError, ConnectionResetError, BrokenPipeError, ValueError, json.JSONDecodeError, TimeOutException) as e:
            # second cheater should not be eliminated
            # if there was already a cheater, ignore
            # drop one player as loser if there are two winners
            if isinstance(e, (OSError, ConnectionResetError, BrokenPipeError)):
                print('[referee: end-game] connection dropped from player')
            else:
                print('referee: {}'.format(e))

    print('[referee] {} {} won'.format('Player' if len(gs.winner) == 1 else 'Players', gs.winner))

    return gs.winner, gs.cheated