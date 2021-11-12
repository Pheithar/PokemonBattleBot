"""
TOURNAMENT BETWEEN ALL BOTS
"""

import sys

# append the path of the parent directory
sys.path.append("..")

from HeuristicBot.HeuristicBot import HeuristicBot
from FullAttackBot.FullAttackBot import FullAttackBot

import asyncio
import time

from poke_env.player.random_player import RandomPlayer
from poke_env.player_configuration import PlayerConfiguration
from poke_env.player.utils import cross_evaluate

from tabulate import tabulate

async def main():

    num_battles = 100

    # We create two players.
    random_player = RandomPlayer(
        battle_format="gen8randombattle",
        player_configuration = PlayerConfiguration("Unown", None)
    )

    heuristic_player = HeuristicBot(
        battle_format="gen8randombattle",
        player_configuration = PlayerConfiguration("Magneton", None)
    )

    max_damage_player = FullAttackBot(
        battle_format="gen8randombattle",
        player_configuration = PlayerConfiguration("Tauros", None)
    )


    players = [random_player, heuristic_player, max_damage_player]
    print(f"Tournament of {num_battles} battles")

    cross_evaluation = await cross_evaluate(players, n_challenges=num_battles)


    # Defines a header for displaying results
    table = [["-"] + [p.username for p in players]]

    # Adds one line per player with corresponding results
    for p_1, results in cross_evaluation.items():
        table.append([p_1] + [cross_evaluation[p_1][p_2] for p_2 in results])

    # Displays results in a nicely formatted table.
    print(tabulate(table))


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
