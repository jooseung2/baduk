point

Implements a single point on a board. 

#### Board

Implements a Board object. It has a field `board`, which is a list of lists of stones, which are either "W", "B", or " "

#### RuleChecker

Implements a class that checks if players have not made any illegal moves, and updates a board after each player's move according to the rule. (https://en.wikipedia.org/wiki/Go_(game)#Rules)

#### Strategy

Implements a class that can take a board and return a move according to a specified strategy. Several strategies are implemented:
- Basic: will place a stone at the most left-top corner
- Capture: will greedily capture if possible, or else it uses Basic.
- Legal Random: chooses a random, empty and legal spot
- Pure Random: chooses a random and empty spot. It may break the rule and lose immediately
- Alpha-Beta Pruning: performs alpha-beta pruning search for a depth k and returns a move with the most scores after k moves.

#### Player

Implements AI players by storing the player's name and its strategy.

#### Referee

Referee object starts and continues a game. It keeps the track of the board history, which player has what color, detects cheating or illegal moves, and evaluates the winner after both players pass their turns.

#### TournamentAdmin

TournamentAdmin.py connects the players through TCP/IP connection. It adminsters a game in a round-robin or single elimination format.

#### `manual_player.py'

Players run this script to participate the tournament and make manual moves.
