BLACK = "B"
WHITE = "W"
EMPTY = " "
PASS = "pass"

STONES = [BLACK, WHITE]
MAYBESTONES = [BLACK, WHITE, EMPTY]

MAX_DEPTH = 1

SIZE = 8192

BOARD_COL_LENGTH = 9
BOARD_ROW_LENGTH = 9

GO_CRAZY_MESSAGE = "GO has gone crazy!"
CANNOT_REMOVE_MESSAGE = "I am just a board! I cannot remove what is not there!"
CANNOT_PLACE_MESSAGE = "This seat is taken!"

END_GAME_PLAYER_MESSAGE = "OK"
INVALID_HISTORY_PLAYER_MESSAGE = "This history makes no sense!"

TIMEOUT_MAKEAMOVE = 2000000000
TIMEOUT_ENDGAME = 50000000

NEG_INF = -1000000000
POS_INF = 1000000000

RESIGN_MESSAGE = "AlphaGo resigns: The result \"{}+Resign\" was added to the game information."