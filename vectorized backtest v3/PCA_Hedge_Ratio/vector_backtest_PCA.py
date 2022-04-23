import numpy as np
import pandas as pd
import yfinance as yf
import statsmodels.api as sm
from sklearn.decomposition import PCA
from scipy import odr
from statsmodels.regression.rolling import RollingOLS
from statsmodels.tsa.api import adfuller
from datetime import *


class Portfolio():

    # should be a collection of pair objects
    # description of overall performance of pairs
    # each pair is backtested by itslef
    # cumulative performance saved in portfolio
    
    def __init__(self, stock_pairs, start, end, ma, alloc):
        self.stock_pairs = stock_pairs
        self.start = start
        self.end = end
        self.ma = ma
        self.alloc = alloc
        self.portfolio = pd.DataFrame()
        
    def makePortfolio(self):
        for x in self.stock_pairs:
            self.portfolio["{}/{}".format(x[0], x[1])] = self.Backtest(x)
        
        self.returns = self.portfolio.sum(numeric_only=True, axis=1)
        self.dot_ret = self.portfolio.dot([1/len(self.stock_pairs) for x in range(len(self.stock_pairs))])
    
    def Backtest(self, pair):
        t = datetime.now()
        
        # get data
        s1 = yf.download(pair[0], self.start, self.end)
        s2 = yf.download(pair[1], self.start, self.end)
        data = pd.DataFrame({'s1':s1['Adj Close'], 's2':s2['Adj Close']}, index = s1.index)

        t2 = datetime.now()
        #####################################################################################
        X1 = np.log(data['s1'])
        X2 = np.log(data['s2'])
        pca_data_in = pd.DataFrame({'X1':X1, 'X2':X2})
        pca_buffer = [0]*self.ma
        data['Hedge Ratio'] = pca_buffer + [PCA(n_components = 2).fit_transform(pca_data_in.iloc[x-self.ma:x])[0][0] for x in range(self.ma, len(pca_data_in))]
        data['Spread'] = (X2 - data['Hedge Ratio']*X1)
        #####################################################################################
        
        # calc z-score
        data['Z_Score'] = (data['Spread']-data['Spread'].rolling(window=self.ma).mean())/data['Spread'].rolling(window=self.ma).std()
        
        t3 = datetime.now()
        # calc ADF test
        adf_buffer = [0]*(self.ma*2)
        data['ADF'] = adf_buffer + [adfuller(data.iloc[(x-self.ma):x]['Hedge Ratio']) for x in range(self.ma+self.ma, len(data))]
        data['ADF lim'] = adf_buffer + [1 if data.iloc[x]['ADF'][0] < data.iloc[x]['ADF'][4]['10%'] else 0 for x in range(self.ma+self.ma, len(data))]
        
        t4 = datetime.now()
        # calc long and short trades
        data['Trade periods short'] = data['Z_Score'].where((data['Z_Score'] >= 2)|(data['Z_Score'] <= 0)).ffill()
        data['Trade periods long'] = data['Z_Score'].where((data['Z_Score'] <= -2)|(data['Z_Score'] >= 0)).ffill()
        data['Trades short'] = (np.sign(data['Trade periods short'])+1)/2
        data['Trades long'] = -(1-(np.sign(data['Trade periods long'])))/2
        data['all trades'] = data['Trades short'] + data['Trades long']
        
        # constrain trades by adf test lims
        data['adf trades'] = data['all trades'].copy().where((np.abs(data['all trades'])==1) & (data['ADF lim'] == 1)).fillna(0)
        
        # cumulative return
        data['pair returns'] = ((((data['s2']-data["Hedge Ratio"]*data['s1']).pct_change()).shift(-1))*data['adf trades']).cumsum()
        
        t5 = datetime.now()
        # return pair returns
#         print("download: ", t2-t)
#         print("z calc: ", t3-t2)
#         print("adf clac: ", t4-t3)
#         print("trade & return calc: ", t5-t4)
        
        return data['pair returns']