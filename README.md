# Vectorized_Backtest_With_Profit_Takes

   - V1: vectorized back test of a simple moving average cross over strategy with profit taking thresholds
        - Comparison between Looped and Vectorised backtest 


   - V2: Vectorsied backtest of a basic stat arb model
        - Long and Short spread trades
        - Only natural entry / exits (z-score +- 2 and ADF < 1%)
   
   
   - To do: 
        - Implement stop loss at max/min Z-score
        - Try rolling orthognal regression instead of rolling OLS
        - portfolio backtest shows that returns are dependent on which stock is set as dependent var
