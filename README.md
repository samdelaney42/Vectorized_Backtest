# Vectorized Backtest

For this project I backtest a simple long short stat arb stretegy using vectorization.

![vector_test](https://github.com/samdelaney42/Vectorized_Backtest_With_Exit_Params/blob/main/data/images/z_score.png)

The simple moving average backtest, is an example of a basic strategy back tested using vectorization.

I build on that with the stat arb walkthrough and back test examples, demonstriting the implemetation of a different strategy using the same technique.

From there, I compare the execution speed of the SMA straregy using vector based and loop based implementations - we find that the vector based implementation executes 50x faster.

Finally, I backtest a portfolio of stock pairs, experementing with different hedge ratio calculations (OLS and TLS).
