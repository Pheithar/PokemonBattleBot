from HeuristicBot import HeuristicBot

import asyncio
import time

from poke_env.player.random_player import RandomPlayer
from poke_env.player_configuration import PlayerConfiguration

async def main():

    num_battles = 100

    # We create two players.
    random_player = RandomPlayer(
        battle_format="gen8randombattle",
    )

    heuristic_player = HeuristicBot(
        battle_format="gen8randombattle",
        player_configuration = PlayerConfiguration("Magneton", None)
    )



    start = time.time()

    # play against the random bot
    await heuristic_player.battle_against(random_player, n_battles=num_battles)

    print(
        "Heuristic player won %d / %d battles [this took %f seconds]"
        % (
            heuristic_player.n_won_battles, num_battles, time.time() - start
        )
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
