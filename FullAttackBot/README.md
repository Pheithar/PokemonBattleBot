# Full Attack Bot

## First attempt: hardcoded bot

This bot is the most basic one. It just going to attack with its strongest move all the time, if it has any attack that has type advantage or is neutral. Otherwise, it will change to the Pokémon in the team with an attack that has advantage. If there is none, it will change to a Pokémon with type advantage. If there is none, it will change to a Pokémon with neutral types. Lastly, if there are none, it will select a random attack.

Here is a simplification in pseudo-code of the algorithm:

```
IF has_attack_with_advantage:
  USE attack_with_advantage (if multiple, the one with the most damage)
ELSE:
  IF pkmn_in_team_has_attack_with_advantage:
    CHANGE pkmn_in_team_with_attack_with_advantage
  ELSE IF pkmn_in_team_has_type_with_advantage:
    CHANGE pkmn_in_team_with_type_with_advantage
  ELSE IF pkmn_in_team_has_not_type_with_disadvantage:
    CHANGE pkmn_in_team_without_type_with_disadvantage
  ELSE:
    USE random_move
```

In this first bot there are many things that are not being taken into account, such as if the changing Pkmn has PP in its move, or if is an attack move, but that does not really matter. For now, this bot is for getting familiar with the library and learn how to use it.

This simple bot, in my quick test, against a random bot, got:

```
Max damage player won 99 / 100 battles [this took 17.091836 seconds]
```
