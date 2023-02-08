from constants import BLACK, WHITE, BOARD_COL_LENGTH, BOARD_ROW_LENGTH, STONES, PASS
from board import Board
from point import Point

"""
boards[0] is the most recent, boards[2] is the least recent
"""

class RuleChecker():
    def __init__(self, ROW = BOARD_ROW_LENGTH, COL = BOARD_COL_LENGTH):
        self.ROW = ROW
        self.COL = COL

    def parse_play(self, user_input):
        """
        input: [stone, [point, [boards]]]
        output: (stone, point, boards)

        removes lists within lists to make loopings easier
        only used to parse the input for the testdriver
        """
        thisturn = user_input[0]
        point = Point.from_str(user_input[1][0])
        boards = [Board(i) for i in user_input[1][1]]
        return [thisturn, point, boards]

    def get_scores(self, board):
        """
        input: board
        output: a dictionary, with keys "B" and "W" and values respective scores
        """
        scores = {BLACK : 0, WHITE : 0}
        for row in range(self.ROW):
            for col in range(self.COL):
                point = Point(row, col)
                if board[point] in STONES:
                    scores[board[point]] += 1
                else:
                    b = board.is_reachable(point, BLACK)
                    w = board.is_reachable(point, WHITE)
                    if b and not w:
                        scores[BLACK] += 1
                    elif w and not b:
                        scores[WHITE] += 1
        return scores

    def check_history(self, stone, boards):
        if len(boards) == 1:
            return self._check_history_length_one(stone, boards)
        elif len(boards) == 2:
            return self._check_history_length_two(stone, boards)
        else:
            return self._check_history_length_three(stone, boards)

    def _check_history_length_one(self, stone, boards):
        return stone == BLACK and boards[0].is_empty()

    def _check_history_length_two(self, stone, boards):
        # check history validity
        if stone != WHITE:
            return False
        if not boards[1].is_empty():
            return False
        added_stones_b0_b1 = self._get_added_stones(boards[0], boards[1])

        if not self._is_legal_progression(boards[0], boards[1], added_stones_b0_b1):
            return False
        if not self._is_valid_turns([self._get_player(added_stones_b0_b1),stone]):
            return False
        return True

    def _check_history_length_three(self, stone, boards):
        # check history validity
        added_stones_b1_b2 = self._get_added_stones(boards[1], boards[2])
     
        if not self._is_legal_progression(boards[1], boards[2], added_stones_b1_b2):
            return False
        added_stones_b0_b1 = self._get_added_stones(boards[0], boards[1])

        if not self._is_legal_progression(boards[0], boards[1], added_stones_b0_b1):
            return False

        if boards[2].is_empty():
            if [self._get_player(added_stones_b1_b2), self._get_player(added_stones_b0_b1), stone] \
                == [PASS, BLACK, WHITE]:
                # cannot pass two times in a row
                return False

        for board in boards:
            if self._get_stones_with_no_liberty(board):
                return False

        if not self._is_valid_turns(
                [self._get_player(added_stones_b1_b2),
                 self._get_player(added_stones_b0_b1),
                 stone]):
            return False
        
        # ko rule
        if boards[0] == boards[2]:
            return False
        return True

    def check_legality(self, stone, point, boards):
        """
        input: stone, point, boards
        output: dictionary, with key "legal" and "new_board"
        "legal" is a bool indicating the legality of the move
        "new_board" is the updated board 

        This function does:
        1) check legality
        2) return updated board, if the move is legal

        had to combine because computation...
        checking legality requires us to actually make a play
        """
        if len(boards) == 1:
            return self._check_legality_for_boards_of_length_one(stone, point, boards)
        elif len(boards) == 2:
            return self._check_legality_for_boards_of_length_two(stone, point, boards)
        else:
            return self._check_legality_for_boards_of_length_three(stone, point, boards)

    def _check_legality_for_boards_of_length_one(self, stone, point, boards):
        result = {"legal":False, "new_board":None}
        if stone == BLACK and boards[0].is_empty():
            new_board, _ = self.get_board_after_adding_stone(boards[0],stone, point)
            result["new_board"] = new_board
            result["legal"] = True
            return result
        return result

    def _check_legality_for_boards_of_length_two(self, stone, point, boards):
        result = {"legal":False, "new_board":None}

        # check history validity
        if stone != WHITE:
            return result
        if boards[0].is_occupied(point):
            return result
        if not boards[1].is_empty():
            return result
        added_stones_b0_b1 = self._get_added_stones(boards[0], boards[1])
        if not self._is_legal_progression(boards[0], boards[1], added_stones_b0_b1):
            return result
        if not self._is_valid_turns([self._get_player(added_stones_b0_b1),stone]):
            return result

        # check new board validity
        new_board, self_captured = \
            self.get_board_after_adding_stone(boards[0], stone, point)
        if self_captured:
            return result

        result["new_board"] = new_board
        result["legal"] = True
        return result

    def _check_legality_for_boards_of_length_three(self, stone, point, boards):
        result = {"legal":False, "new_board":None}

        # check history validity
        if boards[0].is_occupied(point):
            return result
        added_stones_b1_b2 = self._get_added_stones(boards[1], boards[2])
        if not self._is_legal_progression(boards[1], boards[2], added_stones_b1_b2):
            return result
        added_stones_b0_b1 = self._get_added_stones(boards[0], boards[1])
        if not self._is_legal_progression(boards[0], boards[1], added_stones_b0_b1):
            return result

        if boards[2].is_empty():
            if [self._get_player(added_stones_b1_b2), self._get_player(added_stones_b0_b1), stone] \
                == [PASS, BLACK, WHITE]:
                # cannot pass two times in a row
                return result

        for board in boards:
            if self._get_stones_with_no_liberty(board):
                return result
        if not self._is_valid_turns(
                [self._get_player(added_stones_b1_b2),
                 self._get_player(added_stones_b0_b1),
                 stone]):
            return result
            
        # check new board validity
        new_board, self_captured = self.get_board_after_adding_stone(boards[0], stone, point)
        if self_captured:
            return result

        #Check if Ko rule is violated, at this point no consecutive two passes have been made
        if boards[0] == boards[2]:
            return result
        if new_board == boards[1]:
            return result

        result["new_board"] = new_board
        result["legal"] = True
        return result

    def _get_added_stones(self, next_board, prev_board):
        """
        input: new_board, old_board
        output: [
                    {
                        "stone": stone,
                        "point": Point
                    }
                ]
        dictionary with keys "stone" and "point" and values their respective values
        """
        added_stones = []
        for row in range(self.ROW):
            for col in range(self.COL):
                point = Point(row, col)
                if next_board[point] in STONES and not prev_board.is_occupied(point):
                    added_stones.append(
                        {"stone": next_board[point],
                         "point": point})
        return added_stones

    def _is_legal_progression(self, new_board, old_board, added_stones):
        """
        input: board, board, {"stone": .. , "point": ...}
        """
        if len(added_stones) > 1:
            return False
            
        elif len(added_stones) == 1:
            legal_new_board, self_captured = \
                self.get_board_after_adding_stone(old_board, added_stones[0]["stone"], added_stones[0]["point"])
            if self_captured:
                return False

            if new_board != legal_new_board:
                return False

        elif len(added_stones) == 0:
            if new_board != old_board:
                return False
            
        return True

    def get_board_after_adding_stone(self, board, stone, point):
        """
        input: board, stone that has the turn, 
                dictionary of keys "stone" and "point" and values their values
        output: board, self_captured?

        maybepattern
        """
        new_board = board.copy()
        #Step 1: Place a stone
        new_board.place(stone, point)
        #Step 2: Remove any stones of opponent's color that have no liberties
        stones_with_no_liberty = self._get_stones_with_no_liberty(new_board)
        opponent_color = BLACK if stone == WHITE else WHITE
        for stone, pt in [t for t in stones_with_no_liberty if t[0] == opponent_color]:
            new_board.remove(stone, pt)
        #Step 3: If there exists any of own color that have no liberties, self-capture has occured
        stones_with_no_liberty = self._get_stones_with_no_liberty(new_board)
        if [t for t in stones_with_no_liberty if t[0] == stone]:
            return [], True
        # passed
        return new_board, False

    def _is_valid_turns(self, sequence_of_turns):
        """
        sequence of turns is a list of stones that played,
            in the order from the oldest to the latest
        """
        return sequence_of_turns in \
            [[BLACK, WHITE, BLACK],
            [BLACK, PASS, BLACK],

            [WHITE, PASS, WHITE],
            [WHITE, BLACK, WHITE],

            [PASS,BLACK, WHITE],
            [PASS,WHITE, BLACK],

            [PASS,WHITE],
            [BLACK,WHITE]
            ]

    def _get_player(self, added_stones):
        if len(added_stones) == 0:
            return "pass"
        elif len(added_stones) == 1:
            return added_stones[0]["stone"]

    def _get_stones_with_no_liberty(self, board):
        """
        input: board
        output: [(stone, Point), ...]
        """
        stones_with_no_liberty = []
        chain_and_liberties = board.get_chains_and_their_liberties()
        for obj in chain_and_liberties:
            if len(obj["liberties"]) == 0:
                stones_with_no_liberty = stones_with_no_liberty + obj["chain"]
        return stones_with_no_liberty