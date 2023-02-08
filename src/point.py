import json
from constants import BOARD_COL_LENGTH, BOARD_ROW_LENGTH

class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    # string constructor
    @classmethod
    def from_str(cls, str_point):
        # assumes valid point object, in string form.
        row, col = tuple(reversed([int(i) - 1 for i in str_point.split("-")]))
        return cls(row, col)

    @classmethod
    def validate_point_str(cls, point):
        if not isinstance(point, str):
            return False
        coords = point.split('-')
        if len(coords) != 2:
            return False
        try:
            row, col = coords[1], coords[0]
            if int(float(row)) != float(row):
                return False
            if int(float(col)) != float(col):
                return False

            row, col = int(row), int(col)
            if row < 1 or row > BOARD_ROW_LENGTH:
                return False
            if col < 1 or col > BOARD_COL_LENGTH:
                return False
            return True
        except ValueError:
            # when indices are not numeric.
            return False

    def __str__(self):
        return "{}-{}".format(self.col+1, self.row+1)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if self.col > other.col:
            return True
        elif self.col == other.col:
            return self.row > other.row
        else:
            return False
    
    def __le__(self, other):
        return not self.__gt__(other)

    def __lt__(self, other):
        if self.col < other.col:
            return True
        elif self.col == other.col:
            return self.row < other.row
        else:
            return False
    
    def __ge__(self, other):
        return not self.__lt__(other)

    def to_json(self):
        return json.dumps(str(self))

    def inc_row(self):
        return Point(self.row+1, self.col)
    
    def dec_row(self):
        return Point(self.row-1, self.col)
    
    def inc_col(self):
        return Point(self.row, self.col+1)
    
    def dec_col(self):
        return Point(self.row, self.col-1)

# if __name__ == "__main__":
#     p1 = Point(1,5)
#     p2 = Point(1,4)
#     p3 = Point(2,2)
#     print(p1 > p3)