import sys, json, math
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

from wrapper import PlayerWrapper, RefereeWrapper
from player_proxy import PlayerProxy
import referee
from random import randint
from copy import copy
import traceback

referee = RefereeWrapper(referee)


def generate_default_player():
    with open("go.config") as f:
        default_player = json.load(f)["default-player"].split(".")[0]
    mod = __import__(default_player, fromlist=["Player"])

    with open("go-player.config") as f:
        kwargs = {}
        data = json.load(f)

        kwargs["strategy"] = data["strategy"].lower()
        if kwargs["strategy"] in ["alphabeta", "capture"]:
            kwargs["depth"] = data["depth"]

    local_player = PlayerWrapper(getattr(mod, "Player")(**kwargs))
    name = local_player.register()
    return local_player, name


def connect_proxy_player(server):
    client, _ = server.accept()

    player = PlayerWrapper(PlayerProxy(client))
    name = player.register()
    return player, name


def round_robin(players, names):
    """
    input: nothing
    output: dictionary of rankings
    """
    match_history = {}
    for name in names:
        match_history[name] = {"won_against": [], "cheated": False}

    for index1 in range(len(names)):
        for index2 in range(index1 + 1, len(names)):
            p1_name, p2_name = names[index1], names[index2]
            p1, p2 = players[index1], players[index2]

            winner, cheated = referee.play_a_game([(p1, p1_name), (p2, p2_name)])

            if len(winner) == 2:
                coin = randint(0, 1)
                winner_name = winner[coin]
                loser_name = winner[1 - coin]
                print(
                    "[admin] After a thorough consideration, player {} wins. Sorry, {}!".format(
                        winner_name, loser_name
                    )
                )
            else:
                winner_name = winner[0]
                loser_name = p1_name if winner_name == p2_name else p2_name

            match_history[winner_name]["won_against"].append(loser_name)

            if cheated:
                handle_cheater(
                    players, names, match_history, loser_name, index1, index2
                )

    return calculate_ranking_roundRobin(match_history)


def single_elimination(players, names):
    """
    input: nothing
    output: dictionary of rankings
    """
    stage = 1
    cheaters = []
    stage2name = {}
    # key: stage value: list of players' names, who were dropped in that stage
    surviving_players = [player for player in players]
    surviving_names = copy(names)

    while len(surviving_players) > 1:
        # each round
        temp_players = []
        temp_names = []
        for i in range(len(surviving_players) // 2):
            p1_index, p2_index = 2 * i, 2 * i + 1
            p1_name, p2_name = surviving_names[p1_index], surviving_names[p2_index]
            p1, p2 = surviving_players[p1_index], surviving_players[p2_index]

            winner, cheated = referee.play_a_game([(p1, p1_name), (p2, p2_name)])

            # get winner, loser name
            if len(winner) == 2:
                coin = randint(0, 1)
                winner_name = winner[coin]
                loser_name = winner[1 - coin]
                print(
                    "[admin] After a thorough consideration, player {} wins. Sorry, {}!".format(
                        winner_name, loser_name
                    )
                )
            else:
                winner_name = winner[0]
                loser_name = p1_name if winner_name == p2_name else p2_name

            # winner player object appened to temp list
            temp_names.append(winner_name)
            temp_players.append(p2 if winner_name == p2_name else p1)

            # is loser is a cheater, add to cheaters list
            # loser name goes to stage2name
            if cheated:
                cheaters.append(loser_name)
                cheater = p1 if loser_name == p1_name else p2
                cheater.close()

            else:
                if stage in stage2name:
                    stage2name[stage].append(loser_name)
                else:
                    stage2name[stage] = [loser_name]

        # at the end of each round, update players list to temp list (so losers go away)
        surviving_players = temp_players
        surviving_names = temp_names
        stage += 1

    stage2name[stage] = [names[players.index(surviving_players[0])]]
    return calculate_ranking_singleElim(cheaters, stage2name)


def calculate_ranking_roundRobin(match_history):
    player2numofwins = {}

    # rewrite so that the value is ranking, not # of times won
    for name, record in match_history.items():
        if not record["cheated"]:
            player2numofwins[name] = len(record["won_against"])
        else:
            player2numofwins[name] = -1

    # the more wins, higher the ranking (and thus smaller ranking integer value)
    sorted_players = sorted(
        player2numofwins.items(), key=lambda kv: kv[1], reverse=True
    )

    rank, prev = 0, float("inf")
    rankings = {}
    for name, score in sorted_players:
        if score < prev:
            rank += 1
        if rank not in rankings:
            rankings[rank] = [name]
        else:
            rankings[rank].append(name)
        prev = score

    cheaters = [key for (key, value) in match_history.items() if value["cheated"]]
    print(
        "[round robin] number of cheaters: {}\n[round robin] names: {}".format(
            len(cheaters), cheaters
        )
    )
    return rankings


def calculate_ranking_singleElim(cheaters, stage2name):
    rank = 1
    rankings = {}

    sorted_players = sorted(stage2name.items(), key=lambda kv: kv[0], reverse=True)
    for _, losers_in_each_round in sorted_players:

        rankings[rank] = losers_in_each_round
        rank += 1
    rankings[rank] = cheaters
    print(
        "[single elim] number of cheaters: {}\n[single elim] names: {}".format(
            len(cheaters), cheaters
        )
    )
    return rankings


def handle_cheater(players, names, match_history, loser, ind1, ind2):
    # mark as cheater
    match_history[loser]["cheated"] = True

    # close connection to cheater
    cheater_index = names.index(loser)
    players[cheater_index].close()

    # give back points
    for past_losers in match_history[loser]["won_against"]:
        match_history[past_losers]["won_against"].append(loser)

    # replace the cheater, only when it is not the last game
    if not (ind1 == len(names) - 2 and ind2 == len(names) - 1):
        sub_player, sub_name = generate_default_player()
        players[cheater_index] = sub_player
        names[cheater_index] = sub_name
        match_history[sub_name] = {"won_against": [], "cheated": False}


def pretty_print_result(result):
    """
    input: dictionary with keys as rank, and values as list of names of players
    output: void
    """
    print("=" * 45)
    print("result")
    print("=" * 45)
    for key, value in result.items():
        print("Rank {}: {}".format(key, value))


if __name__ == "__main__":
    tournament, number_of_players = sys.argv[1], int(sys.argv[2])
    names, players = [], []

    print(
        "tournament type: {}\nnumber_of_players: {}".format(
            tournament, number_of_players
        )
    )

    server = socket(AF_INET, SOCK_STREAM)
    IP, port = "", 0
    with open("go.config") as f:
        data = json.load(f)
        IP = data["IP"]
        port = data["port"]

    address = (IP, port)

    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(address)
    server.listen()

    for _ in range(number_of_players):
        try:
            player, name = connect_proxy_player(server)
            names.append(name)
            players.append(player)
        except (
            OSError,
            ConnectionResetError,
            BrokenPipeError,
            ValueError,
            json.JSONDecodeError,
        ) as e:
            # traceback.print_exc(e)
            continue

    server.close()  # stop accepting connections

    if len(players) == 0:
        players_needed = 2
    elif len(players) == 1:
        players_needed = 1
    else:
        players_needed = 2 ** math.ceil(math.log2(len(players))) - len(players)

    for _ in range(players_needed):
        player, name = generate_default_player()
        names.append(name)
        players.append(player)

    if tournament in ["--league", "-league"]:
        res = round_robin(players, names)
    elif tournament in ["--cup", "-cup"]:
        res = single_elimination(players, names)

    pretty_print_result(res)

    for player in players:
        player.close()

