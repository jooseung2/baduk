from constants import NEG_INF, POS_INF, PASS, RESIGN_MESSAGE
from rulechecker import RuleChecker
from point import Point
from board import Board
import random
import time
import timeit
from functools import partial

class Strategy():
    def __init__(self, strategy, depth, ROW, COL):
        """
        basic: prioritize lowest column index, and then lowest row index
        capture: prioritize capturing that can happen in one move, else basic strategy
        legal random: places at a random point, only in legal points
        pure random: places at a random point, but in bound
        alpha beta: minimax algorithm
        """
        self.strategy = strategy
        self.rc = RuleChecker(ROW,COL)
        self.ROW = ROW
        self.COL = COL
        self.depth = depth

        self.stone = None
        self.opponent = None
        
        if strategy == "alphabeta":
        # Only the alphabeta player needs it
            self.hoshi = self._get_hoshi()
            self.partitions = []
            self.boards = None
            self.numOfMoves = 0

    def nextmove(self, boards):
        if self.strategy == "basic":
            return self._basic(boards)
        elif self.strategy == "capture":
            return self._capture(boards)
        elif self.strategy == "legalrandom":
            return self._legal_random(boards)
        elif self.strategy == "purerandom":
            return self._pure_random()
        elif self.strategy == "alphabeta":
            return self._alphabeta(boards)

    def _basic(self, boards):
        for point in boards[0].empty_points():
            if self.rc.check_legality(self.stone, point, boards)["legal"]:
                return str(point)
        return PASS

    def _capture(self, boards):
        """
        moves =
        [
            [point1, point2, ...] (from oldest to newest)
            ...
        ]
        """
        def helper(boards, depth):
            moves = []
            board = boards[0]
            if depth < 1:
                return False
            if depth == 1:
                chains = board.get_chains_and_their_liberties()
                opponent_chains = [chain for chain in chains if chain["chain_color"] == self.opponent]
                for chain in opponent_chains:
                    if len(chain["liberties"]) == 1:
                        if self.rc.check_legality(self.stone, chain["liberties"][0], boards)["legal"]:
                            moves.append(chain["liberties"][0])
            if depth > 1:
                # not implemented.
                return helper(boards, depth-1)
            if moves:
                return str(sorted(moves)[0])
            return False

        try_capture = helper(boards, self.depth)
        if not try_capture:
            result = self._basic(boards)
            return result
        else:
            return try_capture
    
    def _legal_random(self, boards):
        available = boards[0].empty_points()
        diceroll = random.randint(0,len(available))
        if diceroll == len(available):
            return PASS
        else:
            return str(available[diceroll])

    def _pure_random(self):
        if random.randint(0,self.ROW * self.COL) < 1:
            # pass with probability 1/(board dimension + 1)
            return PASS
        else:
            return str(Point(random.randint(0,self.ROW-1),random.randint(0,self.COL-1)))

    ############################################################################################################

    # AlphaBetaPlayer implementation
    # It uses minimax algorithm that prunes a path of actions that will never occur

    ############################################################################################################

    def _alphabeta(self, boards):
        current_score = self.rc.get_scores(boards[0])

        start_time = timeit.default_timer()
        # if prev was a pass and i would win, pass
        if len(boards) > 1 and boards[0] == boards[1]:
            if current_score[self.stone] - current_score[self.opponent] > 0:
                print('[AlphaBeta] AlphaBetaPlayer took {} seconds.'.format(round(timeit.default_timer() - start_time,2)))
                return PASS

        # hardcoded to make plays at hoshi for first two moves
        if self.numOfMoves in [0,1]:
            for point in self.hoshi:
                if not boards[0].is_occupied(point):
                    print('[AlphaBeta] AlphaBetaPlayer took {} seconds.'.format(round(timeit.default_timer() - start_time,2)))
                    self.numOfMoves += 1
                    return str(point)

        legalmoves = self.__getLegalMoves(boards, self.stone)
        random.shuffle(legalmoves)

        ##############################################
        ### multiprocessing
        ##############################################

        # save first available moves and boards history

        import multiprocessing
        import numpy
        self.partitions = \
        numpy.array_split(legalmoves, multiprocessing.cpu_count())
        self.boards = boards

        pool = multiprocessing.Pool()
        all_cpu = range(multiprocessing.cpu_count())

        results = pool.map(self.__pool_helper, all_cpu)
        pool.close()
        pool.join()

        best_result = max(results,key=lambda x:x[2])
        cpu, index, _ = best_result[0], best_result[1], best_result[2]

        ##############################################
        ### single process
        ##############################################

        # print('[AlphaBeta] Total branching factor : {}'.format(len(legalmoves)))
        # index, alpha = self.alphabeta_helper(legalmoves, boards)

        if len(legalmoves) > 0:
            print('[AlphaBeta] AlphaBetaPlayer took {} seconds.'.format(round(timeit.default_timer() - start_time,2)))
            return str(self.partitions[cpu][index][0])
            # return str(legalmoves[index][0])
        else:
            print('[AlphaBeta] AlphaBetaPlayer took {} seconds.'.format(round(timeit.default_timer() - start_time,2)))
            return PASS

    def _get_hoshi(self):
        y = self.ROW - 3
        x = self.COL - 3
        hoshi_points = ["4-4","4-{}".format(x),"{}-4".format(y),"{}-{}".format(y,x)]
        random.shuffle(hoshi_points)
        return [Point.from_str(i) for i in hoshi_points]

    def __pool_helper(self, ind):
        process_time = timeit.default_timer()
        partition = self.partitions[ind]
        if len(partition) == 0:
            return ind, 0, NEG_INF
        
        points = [str(point) for point, _ in partition]

        print('[AlphaBeta Process {}] Branching factor: {}\n[Alphabeta Process {}] Assigned points: {}'.format(ind, len(partition),ind,points))

        index, alpha = self.__alphabeta_helper(partition, self.boards)
        print('[AlphaBeta] Process {} took {} seconds.'.format(ind,round(timeit.default_timer() - process_time,2)))

        return ind, index, alpha

    def __h1(self, board):
        # heuristic function
        # evaluates based on the difference btw players' scores
        scores = self.rc.get_scores(board)
        return (scores[self.stone] - scores[self.opponent])

    def __alphabeta_helper(self, legalmoves, boards):
        if len(legalmoves) == 0:
            return self.__h1(boards[0])
        
        alpha = NEG_INF
        beta = POS_INF
        index = None

        for ind, (_, move_result) in enumerate(legalmoves):
            updated_boards = ([move_result["new_board"]] + boards)[:3]
            val = self.__min_value(updated_boards, alpha, beta, 1)
            if(val > alpha):
                index = ind
                alpha = val
        return index, alpha

    def __min_value(self, boards, alpha, beta, depth):
        """
        opponent move
        """
        legalmoves = self.__getLegalMoves(boards, self.opponent)

        if len(legalmoves) == 0 or self.depth == depth:
            return self.__h1(boards[0])
        v = POS_INF

        for _, move_result in legalmoves:
            updated_boards = ([move_result["new_board"]] + boards)[:3]
            val = self.__max_value(updated_boards, alpha, beta, depth+1)
            v = min(val,v)
            if val <= alpha:
                return v
            beta = min(beta,v)
        return v

    def __max_value(self, boards, alpha, beta, depth):
        """
        my move
        """
        legalmoves = self.__getLegalMoves(boards, self.stone)
        if len(legalmoves) == 0 or self.depth == depth:
            return self.__h1(boards[0])

        v = NEG_INF

        for _, move_result in legalmoves:
            updated_boards = ([move_result["new_board"]] + boards)[:3]
            val = self.__min_value(updated_boards, alpha, beta, depth+1)
            v = max(val, v)
            if val >= beta:
                return v
            alpha = max(alpha, v)
        return v
        
    def __getLegalMoves(self, boards, stone):
        """
        returns list of all possible points that will result in the current player's legal play
        """      
        # (Point(x,y), {"legal":True, "new_board":Board()})

        # pair point with a dictionary containing the new board
        point_n_result = map(lambda point: (point, self.__checkLegalityNextMove(boards,point,stone)), boards[0].empty_points())
        # filter the pair for legal new boards
        filtered_point_n_result = [i for i in point_n_result if i[1]["legal"]]
        return filtered_point_n_result

    def __checkLegalityNextMove(self, boards, point, stone):
        """
        player assumes that the board history is correct
        only checks self-capture
        """
        if len(boards) == 1:
            return self.__checkLegalityNextMove_1(boards, point, stone)
        elif len(boards) == 2:
            return self.__checkLegalityNextMove_2(boards, point, stone)
        elif len(boards) == 3:
            return self.__checkLegalityNextMove_3(boards, point, stone)

    def __checkLegalityNextMove_1(self, boards, point, stone):
        result = {"legal":False, "new_board":None}
        new_board, _ = self.rc.get_board_after_adding_stone(boards[0],stone, point)
        result["new_board"] = new_board
        result["legal"] = True
        return result

    def __checkLegalityNextMove_2(self, boards, point, stone):
        result = {"legal":False, "new_board":None}
        new_board, self_captured = \
            self.rc.get_board_after_adding_stone(boards[0], stone, point)
        if self_captured:
            return result

        result["new_board"] = new_board
        result["legal"] = True
        return result
    
    def __checkLegalityNextMove_3(self, boards, point, stone):
        result = {"legal":False, "new_board":None}
        new_board, self_captured = \
            self.rc.get_board_after_adding_stone(boards[0], stone, point)
        if self_captured:
            return result
        if new_board == boards[1]:
            return result

        result["new_board"] = new_board
        result["legal"] = True
        return result