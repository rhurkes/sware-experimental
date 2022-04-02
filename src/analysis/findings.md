# How does SIGN factor in?
```
How many days of each risk have SIGN:
0.02: 0 (0%)
0.05: 0 (0%)
0.10: 49 (40%)
0.15: 24 (96%)
0.30: 3 (100%)
```
```
How does SIGN impact mean tornadoes within the highest risk on 10% days
10%: 1.039832285115304
10% w/SIGN: 2.4958263772954923
```
```Mean EF Rating by Risk
None:           0.43951612903225806
0.02:           0.46194784459819055
0.05:           0.5310753041762578
10% no SIGN:    0.6949685534591195
10% SIGN:       2.045075125208681
0.15:           0.8797709923664122
0.30:           0.5698924731182796
```

- By definition, you will not have SIGN for < 10% risk, and at 15% or greater it's practically a given
- 10% are a 60/40 No SIGN/SIGN
- 2.5x more likely to see a tornado on a 10% SIGN day than just a 10% day
- 10% SIGN is your best chance for a sig tor (7/year), followed by 15% (3/year), and then 10% (10/year)
- 30/45/60% are so incredibly infrequent (< 0 times/year) they should just be an automatic chase
- 2.5x more likely to see a tornado on a 10% day than a 5% day
    - 3.3x for 15%, 5.1x for 30%
- Mean EF rating on 30% days are dragged down by higher number of tornadoes overall (2x that of 10% days)
- The ratios of tornadoes:risk didn't really change when isolated to upslope, which suggests that although it's easier for tornadoes to form, the SPC accounts for that well

```
How many days had each risk as the highest risk:
None: 1169 (45%) (167/year)
0.02: 747 (29%) (106/year)
0.05: 493 (19%) (70/year)
0.10: 120 (4%) (17/year)
    No Sig: 10/year
    Sig: 7/year
0.15: 25 (0%) (3/year)
0.30: 3 (0%) (0/year)
```

# Questions
- How do risks change from 13z to 1630z?
- What are the days worth flying down for?
    - 5/10/10: 30%
    - 5/18/10: 10%
    - 5/19/10: 15%
    - 5/22/10: 10%
    - 5/22/11: 15%
    - 5/24/11: 30%
    - 5/25/11: 30%
    - 5/30/11: 10% Sig
    - 4/14/12: 45%
    - 5/18/13: 10% Sig
    - 5/19/13: 15%
    - 5/20/13: 10% Sig
    - 5/29/13: 15%
    - 5/30/13: 15%
    - 5/31/13: 10% Sig
    - 10/04/13: 10% Sig

One or more days that are 30%+
2 or more days that are 10%+

# TODO
- I can filter outlook by region for things 10% or greater
- Start rendering out all 10, 15, 30, etc. polys to see where they are

# Upslope results
- You have <1 10% day a year and only 5 dedicated 5% days (more will have centroids outside of the upslope zone)
- Because discrete 5%s are so infrequent and the tornadoes/risk is double that of other zones, a 5% in upslope zone is worth watching/chasing
- 10%s are very rarely SIGN (16%) but ~33% more likely to have tornadoes than 10%s in other zones
- SIGNs and 15% are great, but so rare
```
Filtered down to 604 reports (7%)
Tornado days: 190/2557 (7%)
Tornadoes/day: 3

How many tornadoes mean on each risk day:
None: 0
0.02: 1
0.05: 4
0.10: 3
0.15: 8
0.30: 0
SIGN: 6

How many days had each risk as the highest risk:
None: 2423 (94%) (346/year)
0.02: 85 (3%) (12/year)
0.05: 41 (1%) (5/year)
0.10: 6 (0%) (0/year)
0.15: 2 (0%) (0/year)
0.30: 0 (0%) (0/year)

How many days of each risk have SIGN:
0.02: 0 (0%)
0.05: 0 (0%)
0.10: 1 (16%)
0.15: 2 (100%)
0.30: 0 (0%)

How does SIGN impact mean tornadoes within the highest risk on 10% days
10%: 1.0666666666666667
10% w/SIGN: 2.2

How does SIGN impact mean EF rating:
10% no SIGN: 2.6446666666666667
10% SIGN: 5.684000000000001
None: 2.9368661971830994
0.02: 1.6491304347826088
0.05: 1.4787499999999978
0.10: 3.491052631578947
0.15: 4.482941176470588
0.30: 0
```

# N CHASE ALLEY RESULTS
- N Chase Alley just doesn't have 15%+, and you get 1 10% a year
```
Filtered down to 747 reports (9%)
Tornado days: 243/2557 (9%)
Tornadoes/day: 3

How many tornadoes mean on each risk day:
None: 0
0.02: 0
0.05: 2
0.10: 5
0.15: 0
0.30: 0
SIGN: 5

How many days had each risk as the highest risk:
None: 2317 (90%) (331/year)
0.02: 159 (6%) (22/year)
0.05: 69 (2%) (9/year)
0.10: 12 (0%) (1/year)
0.15: 0 (0%) (0/year)
0.30: 0 (0%) (0/year)

How many days of each risk have SIGN:
0.02: 0 (0%)
0.05: 0 (0%)
0.10: 3 (25%)
0.15: 0 (0%)
0.30: 0 (0%)

How does SIGN impact mean tornadoes within the highest risk on 10% days
10%: 1.2
10% w/SIGN: 1.0714285714285714

How does SIGN impact mean EF rating:
10% no SIGN: 2.3762499999999998
10% SIGN: 2.8035714285714293
None: 2.4790395480225995
0.02: 2.0481290322580645
0.05: 3.0799428571428558
0.10: 2.1317460317460313
0.15: 0
0.30: 0
```

# C CHASE ALLEY RESULTS
```
Filtered down to 1232 reports (15%)
Tornado days: 265/2557 (10%)
Tornadoes/day: 4

How many tornadoes mean on each risk day:
None: 0
0.02: 1
0.05: 3
0.10: 6
0.15: 8
0.30: 24
SIGN: 10

How many days had each risk as the highest risk:
None: 2338 (91%) (334/year)
0.02: 103 (4%) (14/year)
0.05: 79 (3%) (11/year)
0.10: 31 (1%) (4/year)
0.15: 4 (0%) (0/year)
0.30: 2 (0%) (0/year)

How many days of each risk have SIGN:
0.02: 0 (0%)
0.05: 0 (0%)
0.10: 11 (35%)
0.15: 3 (75%)
0.30: 2 (100%)

How does SIGN impact mean tornadoes within the highest risk on 10% days
10%: 0.6073619631901841
10% w/SIGN: 1.606060606060606

How does SIGN impact mean EF rating:
10% no SIGN: 2.0290184049079754
10% SIGN: 6.305353535353537
None: 3.3427560521415267
0.02: 2.987906976744187
0.05: 3.393501683501685
0.10: 3.708716577540107
0.15: 6.101764705882352
0.30: 1.8372916666666663
```

# S CHASE ALLEY RESULTS
```
Filtered down to 842 reports (10%)
Tornado days: 245/2557 (9%)
Tornadoes/day: 3

How many tornadoes mean on each risk day:
None: 0
0.02: 0
0.05: 2
0.10: 7
0.15: 4
0.30: 0
SIGN: 7

How many days had each risk as the highest risk:
None: 2339 (91%) (334/year)
0.02: 129 (5%) (18/year)
0.05: 71 (2%) (10/year)
0.10: 17 (0%) (2/year)
0.15: 1 (0%) (0/year)
0.30: 0 (0%) (0/year)

How many days of each risk have SIGN:
0.02: 0 (0%)
0.05: 0 (0%)
0.10: 8 (47%)
0.15: 0 (0%)
0.30: 0 (0%)

How does SIGN impact mean tornadoes within the highest risk on 10% days
10%: 1.446808510638298
10% w/SIGN: 3.3333333333333335

How does SIGN impact mean EF rating:
10% no SIGN: 4.794893617021278
10% SIGN: 17.91611111111111
None: 3.3663723150357985
0.02: 1.9611538461538454
0.05: 2.014438502673797
0.10: 4.280078125
0.15: 4.922499999999999
0.30: 0
```

# MIDWEST RESULTS
```
Filtered down to 1419 reports (17%)
Tornado days: 366/2557 (14%)
Tornadoes/day: 3

How many tornadoes mean on each risk day:
None: 0
0.02: 1
0.05: 2
0.10: 7
0.15: 5
0.30: 0
SIGN: 7

How many days had each risk as the highest risk:
None: 2312 (90%) (330/year)
0.02: 137 (5%) (19/year)
0.05: 84 (3%) (12/year)
0.10: 20 (0%) (2/year)
0.15: 4 (0%) (0/year)
0.30: 0 (0%) (0/year)

How many days of each risk have SIGN:
0.02: 0 (0%)
0.05: 0 (0%)
0.10: 10 (50%)
0.15: 4 (100%)
0.30: 0 (0%)

How does SIGN impact mean tornadoes within the highest risk on 10% days
10%: 0.7058823529411765
10% w/SIGN: 1.8245614035087718

How does SIGN impact mean EF rating:
10% no SIGN: 3.3149019607843138
10% SIGN: 6.56877192982456
None: 3.27858870967742
0.02: 2.6408
0.05: 3.632874493927125
0.10: 4.143096774193549
0.15: 5.06695652173913
0.30: 0
```

# DIXIE ALLEY RESULTS
- Almost double the tornadoes/risk for 10% and 15% compared to other zones
```
Filtered down to 1453 reports (18%)
Tornado days: 268/2557 (10%)
Tornadoes/day: 5

How many tornadoes mean on each risk day:
None: 0
0.02: 0
0.05: 4
0.10: 13
0.15: 13
0.30: 0
SIGN: 13

How many days had each risk as the highest risk:
None: 2294 (89%) (327/year)
0.02: 137 (5%) (19/year)
0.05: 88 (3%) (12/year)
0.10: 27 (1%) (3/year)
0.15: 11 (0%) (1/year)
0.30: 0 (0%) (0/year)

How many days of each risk have SIGN:
0.02: 0 (0%)
0.05: 0 (0%)
0.10: 17 (62%)
0.15: 10 (90%)
0.30: 0 (0%)

How does SIGN impact mean tornadoes within the highest risk on 10% days
10%: 0.49508196721311476
10% w/SIGN: 1.5478260869565217

How does SIGN impact mean EF rating:
10% no SIGN: 2.8046885245901634
10% SIGN: 10.912434782608694
None: 4.1607112068965515
0.02: 2.8198130841121483
0.05: 3.9178260869565222
0.10: 5.917036011080334
0.15: 8.329084967320261
0.30: 0
```