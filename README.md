# Vectorized Backtest

   - Notebook: Basic implementation of a vectorized long / short stat-arb backtest with stoploss parameters 

   - V1: vectorized back test of a simple moving average cross over strategy with profit taking thresholds
        - Comparison between Looped and Vectorised backtest 


   - V2: Vectorsied backtest of a basic stat arb model
        - Long and Short spread trades
        - Only natural entry / exits (z-score +- 2 and ADF < 1%)


   - V3: Implemented rolling PCA (TLS regression) instead of rolling OLS
        - Makes model agnostic to dependent vs independent variable selection 
        - Easier to generate hedge ratio
   
   - To do: 
        - Implement stop loss at max/min Z-score
        - Change return calc. so initial hedge ratio at entry is used for duration of trade, otherwise thisimplies daily rebalance which would have large             costs associated
