import unittest
import json
import sys
import os

sys.path.append(os.path.abspath("../src"))

from point import Point
from board import Board
import tournament_admin
from player import Player


class Test(unittest.TestCase):
    def test_calculateranking_league(self):
        match_history = {
            "first": {"won_against": ["second", "third"], "cheated": False},
            "second": {"won_against": ["third"], "cheated": False},
            "third": {"won_against": [], "cheated": False},
            "cheater1": {"won_against": ["second", "third"], "cheated": True},
            "cheater2": {"won_against": ["first", "third"], "cheated": True},
        }

        rankings = {
            1: ["first"],
            2: ["second"],
            3: ["third"],
            4: ["cheater1", "cheater2"],
        }
        self.assertEqual(
            tournament_admin.calculate_ranking_roundRobin(match_history, "league"), rankings
        )

    def test_calculateranking_cup(self):
        score2name = {
            1: ["first1", "first3", "first4"],
            2: ["second2"],
            3: ["third1", "third2"],
            4: ["fourth1"],
            5: ["fifth1"],
        }
        cheaters = ["first2", "second1"]
        result = tournament_admin.calculate_ranking_singleElim((cheaters, score2name), "cup")

        answer = {
            1: ["fifth1"],
            2: ["fourth1"],
            3: ["third1", "third2"],
            4: ["second2"],
            5: ["first1", "first3", "first4"],
            6: ["first2", "second1"],
        }

        self.assertEqual(answer, result)

    def test_handlecheater(self):
        players, names = [], []
        match_history = {}
        for i in range(8):
            player = Player()
            name = player.register()
            players.append(player)
            names.append(name)
            match_history[name] = {"won_against": [], "cheated": False}
            if i == 6:
                match_history[name]["won_against"] = [names[1], names[0]]

        cheater_name = ""

        for i1 in range(len(names)):
            for i2 in range(i1 + 1, len(names)):
                if i1 == 2 and i2 == 6:
                    winner_name, loser_name = names[i1], names[i2]
                    cheater_name = loser_name
                    tournament_admin.handle_cheater(
                        players, names, match_history, winner_name, loser_name, i1, i2
                    )
                if i1 == 6:
                    # check replacement
                    self.assertNotEqual(names[i1], cheater_name)

        # check flag
        self.assertTrue(match_history[cheater_name]["cheated"])

        # check giving back points
        self.assertEqual(match_history[names[0]]["won_against"], [cheater_name])
        self.assertEqual(match_history[names[1]]["won_against"], [cheater_name])

        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
