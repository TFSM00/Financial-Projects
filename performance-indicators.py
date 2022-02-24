from calendar import c
import pandas_datareader as pdr
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

start = dt.datetime(2015,1,1)
end = dt.datetime(2022,1,1)

data = pdr.get_data_yahoo(["AAPL","MSFT", "IBM"], start, end, interval="d")
data = data["Adj Close"]


def CAGR(data):
    df = data.copy()
    df = np.log(df/df.shift())
    df = (1 + df).cumprod()
    trading_days = 252
    n = len(df)/trading_days
    cagr = list((df.iloc[-1])**(1/n) - 1)
    return cagr


def annualizedVol(data):
    df = data.copy()
    df = np.log(df/df.shift())
    trading_days = 252
    vol = list(df.std() * np.sqrt(trading_days))
    return vol

def sharpeRatio(data, rf):
    df = data.copy()
    sharpe = (CAGR(df) - rf)/annualizedVol(df)
    return sharpe

def sortinoRatio(data, rf):
    df1 = data.copy()
    df = np.log(df1/df1.shift())
    df = np.where(df<0, df, 0)
    df = pd.DataFrame(df, columns=["AAPL","IBM","MSFT"])
    negative_vol = list(df.std() * np.sqrt(252))
    sortinos = []
    for i in range(0,3):
        sortinos.append( (CAGR(df1)[i] - rf)/negative_vol[i] )
        
    return sortinos

def maxDrawdown(data):
    df = data.copy()

    df = np.log(df/df.shift())
    df_cum_rets = (1 + df).cumprod()
    df_cum_max = df_cum_rets.cummax()
    df_drawdown = df_cum_max - df_cum_rets
    df_drawdown_pct = df_drawdown / df_cum_max
    max_dd = df_drawdown_pct.max()

    #plt.plot(df["drawdown_pct"])
    #plt.show()
    return max_dd
 

def calmarRatio(data, rf):
    df = data.copy()
    calmars = []
    for i in range(0,3):
        calmars.append ( (CAGR(df)[i] - rf) / maxDrawdown(data)[i] )
    return calmars

def valueAtRisk(data):
    df = data.copy()
    df = np.log(df/df.shift())
    df = df[1:]
    
    sorted_rets = pd.DataFrame(columns=["AAPL","IBM","MSFT"])
    for i in ["AAPL","IBM","MSFT"]:
        sorted_rets[i] = df[i].sort_values(ascending=True)

    print(sorted_rets)
    var90s = []
    var95s = []
    var99s = []
    cvar90s = []
    cvar95s = []
    cvar99s = []

    for i in ["AAPL","IBM","MSFT"]:
        var90 = sorted_rets[i].quantile(0.1)
        var95 = sorted_rets[i].quantile(0.05)
        var99 = sorted_rets[i].quantile(0.01)
        cvar90 = sorted_rets[i][sorted_rets[i] <= var90].mean()
        cvar95 = sorted_rets[i][sorted_rets[i] <= var95].mean()
        cvar99 = sorted_rets[i][sorted_rets[i] <= var99].mean()
        var90s.append(var90)
        var95s.append(var95)
        var99s.append(var99)
        cvar90s.append(cvar90)
        cvar95s.append(cvar95)
        cvar99s.append(cvar99)
    
    return [var90s, var95s, var99s, cvar90s, cvar95s, cvar99s]


#tbl["Conditional Value at Risk (Expected Loss)"] = [cvar90, cvar95, cvar99]
print(sortinoRatio(data, 0.03))