# DMAC-BTC-Trading-Example-With-Tuning

The original version of this code is from https://www.datacamp.com/community/tutorials/finance-python-trading#tradingstrategy

I would recommend reviewing that page at least briefly before playing with this code as it will make more sense.

I took the code and modified it to show returns on BTC. From that point the code was modified to auto tune the short and long moving averages to produce optimum gains.

All of this culimates in the simple-strat-loop-backtest-time-segments.py
version which will go through all of the years from 2010 to 2018 and tune the DMAC, dual moving average crossover for the best gains and produce a text dump of the parameters for the moving averages in days and the gains in $, starting with $100000.

It also shows the HODL gains for comparison. As if you bought on Jan 1 and held for the year.

EXAMPLE OUTPUT:

Get Data for 2018
Run Model
Count,Short AVG,Long AVG,Best Bank 1 1 1 100000.0
Count,Short AVG,Long AVG,Best Bank 2 1 4 202680.224609375
Count,Short AVG,Long AVG,Best Bank 3 1 7 272006.0546875
Count,Short AVG,Long AVG,Best Bank 4 1 21 279009.0576171875
Count,Short AVG,Long AVG,Best Bank 5 2 3 302478.3447265625
Count,Short AVG,Long AVG,Best Bank 6 34 27 310013.9892578125
Count,Short AVG,Long AVG,Best Bank 7 34 29 312617.0166015625
Count,Short AVG,Long AVG,Best Bank 8 34 31 322783.0322265625
Count,Short AVG,Long AVG,Best Bank 9 34 32 400046.0205078125
Count,Short AVG,Long AVG,Best Bank 10 35 20 410732.8369140625
Count,Short AVG,Long AVG,Best Bank 11 35 26 437209.9365234375
Count,Short AVG,Long AVG,Best Bank 12 35 30 454225.0244140625
HODL Gains: 0.2684678826353506

I have included simple-strat.py, which is the same code as the Datacamp article writes about for reference.

Beyond that and the second mod to it, the code goes into various types of looping to optimize the parameters for the DMAC. Most do brute force looping and simple-strat-stoch-backtest.py does a random selection.

A TBD would be to use differential evolution to pick the best average parameters. This would be more efficient than stochastic methods or brute force. 