from FullAttackBot import FullAttackBot

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

    # Rhino, because it goes head first (I know is stupid)
    max_damage_player = FullAttackBot(
        battle_format="gen8randombattle",
        player_configuration = PlayerConfiguration("Rhino", None)
    )



    start = time.time()

    # play against the random bot
    await max_damage_player.battle_against(random_player, n_battles=num_battles)

    print(
        "Max damage player won %d / %d battles [this took %f seconds]"
        % (
            max_damage_player.n_won_battles, num_battles, time.time() - start
        )
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
