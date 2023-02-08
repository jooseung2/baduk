import json

from constants import BOARD_ROW_LENGTH, BOARD_COL_LENGTH, EMPTY, BLACK, WHITE, CANNOT_PLACE_MESSAGE, CANNOT_REMOVE_MESSAGE, MAYBESTONES
from point import Point
from copy import deepcopy
import queue

class Board:
    def __init__(self, board, ROW=BOARD_ROW_LENGTH, COL=BOARD_COL_LENGTH):
        self.board = board
        self.ROW = ROW
        self.COL = COL

    @classmethod
    def empty(cls,ROW=BOARD_ROW_LENGTH, COL=BOARD_COL_LENGTH):
        return Board(\
            [[EMPTY for _ in range(COL)] for _ in range(ROW)], ROW, COL
        )

    @classmethod
    def validate_board(cls, board):
        if not isinstance(board, Board):
            return False
        if len(board.board) != BOARD_ROW_LENGTH:
            return False

        for i in board.board:
            if not isinstance(i, list):
                return False
            if len(i) != BOARD_COL_LENGTH:
                return False

        for row in range(BOARD_ROW_LENGTH):
            for col in range(BOARD_COL_LENGTH):
                if board[row][col] not in MAYBESTONES:
                    return False
        return True

    @classmethod
    def validate_boards(cls, boards):
        if not isinstance(boards, list): return False
        if not 0 < len(boards) < 4: return False

        for i in boards:
            if not cls.validate_board(i):
                return False

        return True

    @classmethod
    def validate_board_list(cls, board):
        if not isinstance(board, list):
            return False
        if len(board) != BOARD_ROW_LENGTH:
            return False

        for i in board:
            if not isinstance(i, list):
                return False
            if len(i) != BOARD_COL_LENGTH:
                return False

        for row in range(BOARD_ROW_LENGTH):
            for col in range(BOARD_COL_LENGTH):
                if board[row][col] not in MAYBESTONES:
                    return False
        return True

    @classmethod
    def validate_boards_list(cls, boards):
        if not isinstance(boards, list):
            return False
        if not 0 < len(boards) < 4:
            return False

        for i in boards:
            if not cls.validate_board_list(i):
                return False

        return True

    def __str__(self):
        """
        for debugging purpose.
        board will pretty-print if wrapped in str operator
        """
        result = ""
        form = ('{:>2} '*(self.COL+1)).rstrip()
        columns = [" "] + list(range(1,self.COL+1))

        result += form.format(*columns)+'\n'

        for ind, row in enumerate(self.board):
            row_shape = ['\u25cf' if i == BLACK else '\u25cb' if i == WHITE else EMPTY for i in row]
            result += form.format(ind+1,*row_shape)+'\n'
        return result

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if self.ROW != other.ROW or self.COL != other.COL:
            return False
        
        for i in range(self.ROW):
            for j in range(self.COL):
                if self.board[i][j] != other[i][j]:
                    return False
        return True

    def __ne__(self,other):
        return not self.__eq__(other)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.board[index]
        elif isinstance(index, Point):
            row,col = index.row, index.col
            return self.board[row][col]

    def __setitem__(self, point, stone):
        if isinstance(point, Point):
            row, col = point.row, point.col
            self.board[row][col] = stone
        elif isinstance(point, int):
            pass

    def is_empty(self):
        for i in self.board:
            for j in i:
                if j != EMPTY:
                    return False
        return True

    def copy(self):
        return Board(deepcopy(self.board),self.ROW,self.COL)

    def to_list(self):
        return self.board

    def is_occupied(self, point):
        return not self[point] == EMPTY
    
    def occupies(self, stone, point):
        return self[point] == stone

    def is_reachable(self, point, maybestone):
        def add_neighbors(stack, pt, visited):
            if 0 <= pt.row < self.ROW and 0 <= pt.col < self.COL:
                if pt not in visited:
                    stack.append(pt)
        
        stone = self[point]
        stack = [point]
        visited = set()
        while stack:
            curr = stack.pop()
            visited.add(curr)
            if self[curr] == maybestone:
                return True
            elif self[curr] == stone:
                add_neighbors(stack, curr.inc_row(), visited)
                add_neighbors(stack, curr.dec_row(), visited)
                add_neighbors(stack, curr.inc_col(), visited)
                add_neighbors(stack, curr.dec_col(), visited)
        return False
    
    def place(self, stone, point):
        if self.is_occupied(point):
            return CANNOT_PLACE_MESSAGE
        self[point] = stone
        return self

    def remove(self, stone, point):
        if self.occupies(stone, point):
            self[point] = EMPTY
            return self
        else:
            return CANNOT_REMOVE_MESSAGE
    
    def get_points(self, maybestone):
        result = []
        for row in range(self.ROW):
            for col in range(self.COL):
                if self[Point(row,col)] == maybestone:
                    result.append(str(Point(row, col)))
        return sorted(result)

    def get_chains_and_their_liberties(self):
        """
        input: None
        output: [{"chain_color":STONE, "chain":[(STONE, point), ...], "liberties":[point, ...]}]
        """
        def get_neighbors(point, visited):
            def append_if_valid_point(arr, pt1, visited):
                def valid_point(pt2):
                    return 0 <= pt2.row < self.ROW and 0 <= pt2.col < self.COL
                if valid_point(pt1) and pt1 not in visited:
                    arr.append(pt1)

            neighbors = []
            append_if_valid_point(neighbors, point.dec_row(), visited)
            append_if_valid_point(neighbors, point.inc_row(), visited)
            append_if_valid_point(neighbors, point.dec_col(), visited)
            append_if_valid_point(neighbors, point.inc_col(), visited)
            return neighbors
        
        def get_single_chain(point):
            """
            input: point
            output: [(stone, point), ...] [point, ...]
            """
            q = queue.Queue()
            stone = self[point]
            visited = set()
            connected_stones = set()
            liberties = set()
            q.put(point)
            while not q.empty():
                curr = q.get()
                if curr in visited:
                    continue
                visited.add(curr)
                curr_stone = self[curr]
                if curr_stone == stone:
                    connected_stones.add((curr_stone, curr))
                    for neighbor in get_neighbors(curr, visited):
                        q.put(neighbor)
                else:
                    if curr_stone == EMPTY:
                        liberties.add(curr)
            return sorted(list(connected_stones)), sorted(list(liberties))
        
        liberty_board = Board.empty()
        unique_id = 0
        chain_and_liberties = []
        for x in range(self.COL):
            for y in range(self.ROW):
                curr = Point(x,y)
                if self.is_occupied(curr) and not liberty_board.is_occupied(curr):
                    conneted_stones, liberties = get_single_chain(curr)
                    chain_id = self[curr] + str(unique_id)
                    for _, pt in conneted_stones:
                        liberty_board = liberty_board.place(chain_id, pt)
                    chain_and_liberties.append({"chain_color":self[curr], "chain":conneted_stones, "liberties":liberties})
                    unique_id += 1
        return chain_and_liberties

    def empty_points(self):
        result = []
        for col in range(self.COL):
            for row in range(self.ROW):
                if self[Point(row,col)] == EMPTY:
                    result.append(Point(row,col))
        return result

# if __name__ == "__main__":
#     b1 = Board.empty()
#     b1[Point(1,2)] = BLACK
#     b1[Point(1,3)] = BLACK
#     b1[Point(1,4)] = BLACK
#     print(b1)
#     print(b1.is_occupied(Point(1,2)))
#     # print(b1.is_reachable(Point(1,5),EMPTY))
#     print(b1.place(BLACK, Point(1,5)))
#     print(b1.get_chains_and_their_liberties())
