from poke_env.player.env_player import Gen8EnvSinglePlayer
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import LinearAnnealedPolicy, EpsGreedyQPolicy
from tensorflow.keras.optimizers import Adam
from poke_env.player.random_player import RandomPlayer
import numpy as np

#Can't / won't make this one work. I'm not that interested in thsi one. Maybe is compatibility between versions.


class SimpleRLPlayer(Gen8EnvSinglePlayer):
    def embed_battle(self, battle):
        # -1 indicates that the move does not have a base power
        # or is not available
        moves_base_power = -np.ones(4)
        moves_dmg_multiplier = np.ones(4)
        for i, move in enumerate(battle.available_moves):
            moves_base_power[i] = move.base_power / 100 # Simple rescaling to facilitate learning
            if move.type:
                moves_dmg_multiplier[i] = move.type.damage_multiplier(
                    battle.opponent_active_pokemon.type_1,
                    battle.opponent_active_pokemon.type_2,
                )

        # We count how many pokemons have not fainted in each team
        remaining_mon_team = len([mon for mon in battle.team.values() if mon.fainted]) / 6
        remaining_mon_opponent = (
            len([mon for mon in battle.opponent_team.values() if mon.fainted]) / 6
        )

        # Final vector with 10 components
        return np.concatenate(
            [moves_base_power, moves_dmg_multiplier, [remaining_mon_team, remaining_mon_opponent]]
        )

    def compute_reward(self, battle) -> float:
        return self.reward_computing_helper(
            battle,
            fainted_value=2,
            hp_value=1,
            victory_value=30,
        )

env_player = SimpleRLPlayer(battle_format="gen8randombattle")


# Output dimension
n_action = len(env_player.action_space)

model = Sequential()
model.add(Dense(128, activation="elu", input_shape=(1, 10,)))

# Our embedding have shape (1, 10), which affects our hidden layer dimension and output dimension
# Flattening resolve potential issues that would arise otherwise
model.add(Flatten())
model.add(Dense(64, activation="elu"))
model.add(Dense(n_action, activation="linear"))

memory = SequentialMemory(limit=10000, window_length=1)

# Simple epsilon greedy
policy = LinearAnnealedPolicy(
    EpsGreedyQPolicy(),
    attr="eps",
    value_max=1.0,
    value_min=0.05,
    value_test=0,
    nb_steps=10000,
)

# Defining our DQN
dqn = DQNAgent(
    model=model,
    nb_actions=18,
    policy=policy,
    memory=memory,
    nb_steps_warmup=1000,
    gamma=0.5,
    target_model_update=1,
    delta_clip=0.01,
    enable_double_dqn=True,
)

dqn.compile(Adam(lr=0.00025), metrics=["mae"])


def dqn_training(player, dqn, nb_steps):
    dqn.fit(player, nb_steps=nb_steps)

    # This call will finished eventual unfinshed battles before returning
    player.complete_current_battle()

opponent = RandomPlayer(battle_format="gen8randombattle")

# Training
env_player.play_against(
    env_algorithm=dqn_training,
    opponent=opponent,
    env_algorithm_kwargs={"dqn": dqn, "nb_steps": 100000},
)
