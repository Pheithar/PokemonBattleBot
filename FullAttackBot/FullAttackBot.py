from poke_env.player.player import Player


class FullAttackBot(Player):
    def choose_move(self, battle):

        # Get only attacks that do damage. This bot is only aggresive, no stats bullshit
        attack_moves = [move for move in battle.available_moves if move.base_power > 0]

        # Get the types of the oposing pkmn
        enemy_types = battle.opponent_active_pokemon.types

        if len(attack_moves) > 0:

            # Get the move that has more damage multiplier
            best_move = max(attack_moves, key=lambda move: move.type.damage_multiplier(*enemy_types))

            # Only use the attack if its effective
            if best_move.type.damage_multiplier(*enemy_types) >= 1:
                return self.create_order(best_move)

        # Pokemon to be switched
        switch_to = None

        # best attack decided by multiplier
        best_attack = (None, 1)

        # Loop through the possible switches to see if any has move with type advantage
        for pkmn in battle.available_switches:

            best_move = max(list(pkmn.moves.values()),key=lambda move: move.type.damage_multiplier(*enemy_types))

            if best_move.type.damage_multiplier(*enemy_types) > best_attack[1]:
                switch_to = pkmn
                best_attack = (best_move, best_move.type.damage_multiplier(*enemy_types))

        # If there is a Pkmn that has a move with type advantage change to it
        if switch_to:
            return self.create_order(switch_to)

        best_mult = 1

        # Loop through the possible switches to see if their types advantage
        for pkmn in battle.available_switches:
            mult = pkmn.type_1.damage_multiplier(*enemy_types)

            if pkmn.type_2:
                mult *= pkmn.type_2.damage_multiplier(*enemy_types)

            if mult >= best_mult:
                switch_to = pkmn
                best_mult = mult

        if switch_to:
            return self.create_order(switch_to)

        # If nothing else was available, just make a random move
        return self.choose_random_move(battle)
