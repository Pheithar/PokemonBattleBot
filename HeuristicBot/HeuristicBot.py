import poke_env
from poke_env.player.player import Player


GENERAL_STATS = {
    -6: 2/8, -5: 2/7, -4: 2/6, -3: 2/5, -2: 2/4, -1: 2/3,
    0: 2/2,
    1: 3/2, 2: 4/2, 3: 5/2, 4: 6/2, 5: 7/2, 6: 8/2
}

PRECISION_STAT = {
    -6: 3/9, -5: 3/8, -4: 3/7, -3: 3/6, -2: 3/5, -1: 3/4,
    0: 3/3,
    1: 4/3, 2: 5/3, 3: 6/3, 4: 7/3, 5: 8/3, 6: 9/3
}

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

class HeuristicBot(Player):

    def choose_move(self, battle):

        rival_pkmn = battle.opponent_active_pokemon

        heuristic = []

        for pkmn in battle.team.values():
            # Check only not fainted Pokemon (status 2 = FNT (fainted))
            if not pkmn.status or pkmn.status.value != 2:
                moves_atck_at = []
                for move in pkmn.moves.values():
                    moves_atck_at.append(self.calculate_attack(move,
                                                                pkmn,
                                                                rival_pkmn))
                    max_atck_att = max(moves_atck_at)

                    bench = self.calculate_benched(pkmn)

                    pkmn_char = self.calculate_characteristic(pkmn, rival_pkmn)

                    # h = max_atck_att - bench + pkmn_char
                    h = max_atck_att - bench
                    heuristic.append((pkmn, move, h))


        sorted_moves = sorted(heuristic, key=lambda x: x[2], reverse=True)

        counter = 0

        while counter < len(sorted_moves):
            best_move = sorted_moves[counter]

            if best_move[0].active and best_move[1] in battle.available_moves:
                return self.create_order(best_move[1])
            if not best_move[0].active and best_move[0] in battle.available_switches:
                return self.create_order(best_move[0])
            counter += 1

        return self.choose_random_move(battle)

    def normalize_stat(self, pokemon, stat):

        atck = pokemon.stats["atk"]
        sp_atck = pokemon.stats["spa"]

        return pokemon.stats[stat] / (atck + sp_atck)

    def calculate_attack(self, move, ally, enemy):
        """Calculate the attack features"""

        atck_adv_type = move.type.damage_multiplier(*enemy.types)
        atck_pwd = move.base_power / 100
        atck_prec = move.accuracy

        is_phys = move.category.value == 1
        is_spec = move.category.value == 2

        boost = 1

        value_stat = 0

        if is_phys:
            atck_stat = ally.boosts["atk"]
            def_stat = enemy.boosts["def"]

            boost *= GENERAL_STATS[clamp(atck_stat + def_stat, -6, 6)]

            value_stat = self.normalize_stat(ally, "atk")

        if is_spec:
            atck_stat = ally.boosts["spa"]
            def_stat = enemy.boosts["spd"]

            boost *= GENERAL_STATS[clamp(atck_stat + def_stat, -6, 6)]

            value_stat = self.normalize_stat(ally, "spa")

        ally_acc = ally.boosts["accuracy"]
        enemy_eva = enemy.boosts["evasion"]

        boost_prec = GENERAL_STATS[clamp(ally_acc + enemy_eva, -6, 6)]

        stab = 1

        if move.type in ally.types:
            stab = 1.5

        total_prec = clamp(atck_prec * boost_prec, 0, 1)

        return atck_pwd * total_prec * atck_adv_type * stab * value_stat * boost


    def calculate_benched(self, ally):
        """Calculate additional values if the Pokemon is benched"""

        in_bench = 0

        if not ally.active:
            in_bench = 1

        hp = ally.current_hp_fraction

        return in_bench * (1 - hp)

    def calculate_characteristic(self, ally, enemy):
        """Calculate Pokemon characteristics"""

        stats = 0
        if ally.status:
            stats = 1

        pkmn_adv_type = 1

        for type in ally.types:
            if type:
                pkmn_adv_type *= type.damage_multiplier(*enemy.types)

        pkmn_adv_type_move = [1]
        for move in enemy.moves.values():
            pkmn_adv_type_move.append(move.type.damage_multiplier(*ally.types))

        max_pkmn_adv_type_move = max(pkmn_adv_type_move)

        return -stats + pkmn_adv_type - max_pkmn_adv_type_move
