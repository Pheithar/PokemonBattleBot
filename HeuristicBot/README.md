# Heuristic bot

This bot is going to run an easy heuristic for each of its options, and decide in consequence which one to do. Still, this one does not use machine learning, as the value in the heuristic is going to be hard-coded, but it would allow it to take more things into account.


## Features

 - Attack Attributes
```
atck_adv_type = atack type advantage against rival Pokemon
atck_pwd = atack base power / 100
atck_prec = attack precision
boosts_{stat} = Boost on {stat}. To see how that works, see Boosts
value_stat = Value of the stat (Attack or Special Attack) that is used for performing the attack. To see how that works, see Value Stat
stab = Same type attack bonus
```

 - Benched Pokemon Information
```
in_bench = Whether or not the Pokemon is in available in the bench
hp = percentage of remaining health
```

 - Pokemon Characteristics
```
status = Whether or not the ally Pokemon has a status condition
pkmn_adv_type = Pokemon type advantage against rival
pkmn_adv_type_{move} = Type advantage of the Pokemon against the move {move}
```


## Heuristic

As seen previously, for each attack, 3 types of features are used. The Attack Attributes is calculates as

```
atck_att = atck_pwd * (atck_prec * boost_prec) * atck_adv_type * stab * value_stat * boost_{atck/spe.atck}
```

It is just a multiplication of all the values of the attack. stab can be either 1 or 1.5 if the Pokemon shares type with the attack. The boost is calculated depending on the type of attack. The precision multiplied by its boost can be, at most, 1.

The benched information is only used if it is benched, and it is in negative as it takes a turn to change the Pokemon, so it is not ideal. The lower the health, the worst to.

```
bench = in_bench * (1 - hp)
```   

In bench is either 0 or 1.

Lastly, the Pokemon Characteristics. The status is a negative effect, and therefore is in negative.

Then the type advantage is taken into account, being multiplied by the worst type advantage of the rival Pokemon attacks against the Pokemon (this are not known at the start, and changes each turn).

```
pkmn_char = -stats + pkmn_adv_type * MAX(pkmn_adv_type_{move})
```

The final heuristic looks like:

```
h = atck_att - bench + pkmn_char
```

## Boosts

 - Attack, Special Attack, Defense and Special Defense Boost

 | -6 | -5 | -4 | -3 | -2 | -1 | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
 |----|----|----|----|----|----|---|---|---|---|---|---|---|
 |2/8 |2/7 |2/6 |2/5 |2/4 |2/3 |2/2|3/2|4/2|5/2|6/2|7/2|8/2|

 - Precision and Evasion Boost

 | -6 | -5 | -4 | -3 | -2 | -1 | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
 |----|----|----|----|----|----|---|---|---|---|---|---|---|
 |3/9 |3/8 |3/7 |3/6 |3/5 |3/4 |3/3|4/3|5/3|6/3|7/3|8/3|9/3|


 The total boost is calculated as the attacking proper boost (Attack, Special Attack or Precision) plus the rival Pokemon boost (Defense, Special Defense or Evasion). It can never be greater than 6 or lower than -6.


## Value Stat

To have a value that can be compared between different Pokemon, the value stat is going to be calculated as the stat value (Attack or Special Attack), divided by the sum of of both stats.

This can be understood as a normalization of the attack stat.


## Results

This bot, against a random bot, gets:

```
Heuristic player won 87 / 100 battles [this took 16.374792 seconds]
```

Which is lower than expected, but if the heuristic is changed a bit, such that the final heuristic is:

```
h = atck_att - bench
```

Then the results go a bit higher with:

```
Heuristic player won 90 / 100 battles [this took 14.810259 seconds]
```

Which is still lower than expected.
