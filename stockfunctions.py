#Imports
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr
from pandas.testing import assert_frame_equal
import matplotlib.pyplot as plt
import yahoo_fin.stock_info as si  #* imports fundamentals package
import pandas as pd
from sys import argv #* lets me check for arguments in the cmd
yf.pdr_override()

#* Stocks-related functions

def stockprice_alltime_plot(ticker):
    data=yf.download(str(ticker), period="max")
    df=pd.DataFrame(data)
    df.plot(y="Adj Close")
    plt.grid()
    plt.show()

def stockprice_period_plot(ticker, startdate, enddate):
    data=yf.download(str(ticker), start=startdate, end=enddate)
    df=pd.DataFrame(data)
    df.plot(y="Adj Close")
    plt.grid()
    plt.show()

def multiplestockprice_alltime_plot(tickers):
    data=yf.download(tickers, period="max")
    df=pd.DataFrame(data)
    df.plot(y="Adj Close")
    plt.grid()
    plt.show()

def multiplestockprice_period_plot(tickers, startdate, enddate):
    data=yf.download(tickers, start=startdate, end=enddate)
    df=pd.DataFrame(data)
    df.plot(y="Adj Close")
    plt.grid()
    plt.show()

def stockinfo(ticker):
    ref=yf.Ticker(ticker)
    a=ref.info
    return a
    
def divi_splits_table(ticker):
    ref=yf.Ticker(ticker)
    a=ref.actions
    print(a)

def divi_plot(ticker):
    ref=yf.Ticker(ticker)
    a=ref.actions
    df=pd.DataFrame(a)
    df.plot(y="Dividends")
    plt.grid()
    plt.show()

def last4year_earnings(ticker):
    tickers=yf.Ticker(ticker)
    a=tickers.earnings  

def last4quarters_earnings(ticker):
    tickers=yf.Ticker(ticker)
    a=tickers.quarterly_earnings
    print(a)

def last4year_financials(ticker):
    tickers=yf.Ticker(ticker)
    a=tickers.financials
    print(a)

def last4quarters_financials(ticker):
    tickers=yf.Ticker(ticker)
    a=tickers.quarterly_financials
    print(a)

def major_holders(ticker):
    
    print("\n\n")
    tickers=yf.Ticker(ticker)
    a=tickers.major_holders
    print(a)   

def institutional_holders(ticker):
    
    print("\n\n")
    tickers=yf.Ticker(ticker)
    a=tickers.institutional_holders
    print(a)   

def last4year_balance_sheet(ticker):
   
    print("\n\n")
    tickers=yf.Ticker(ticker)
    a=tickers.balance_sheet
    print(a)

def last4quarters_balance_sheet(ticker):
   
    print("\n\n")
    tickers=yf.Ticker(ticker)
    a=tickers.quarterly_balance_sheet
    print(a)

def last4year_cashflow(ticker):
    
    print("\n\n")
    tickers=yf.Ticker(ticker)
    a=tickers.cashflow
    print(a)

def last4quarters_cashflow(ticker):
   
    print("\n\n")
    tickers=yf.Ticker(ticker)
    a=tickers.quarterly_cashflow
    print(a)

def ethical_sustainability(ticker):
    
    print("\n")
    print("Ethics Report for "+ticker+"\n")
    tickers=yf.Ticker(ticker)
    a=tickers.sustainability
    print(a)

def recomendations(ticker):
    
    print("\n")
    tickers=yf.Ticker(ticker)
    try:
        a=tickers.recomendations
        print(a)
    except AttributeError:
        print("No recomendations for this company")

def calendar(ticker):
   
    print("\n")
    tickers=yf.Ticker(ticker)
    a=tickers.calendar
    print(a)    

def option_chain(ticker):
    
    print("\n")
    tickers=yf.Ticker(ticker)
    a=tickers.options
    alist=list(a)
    print("Next Options Expiry Dates:\n\n")
    for item in alist:
        print(item)

    print("\n")
    date=input("Insert a expiry date: ")
    b=tickers.option_chain(date)
    print("\n\n")
    print("Call options\n")
    c=b.calls
    print(c)
    print("\n\n")
    print("Put options\n")
    d=b.puts
    print(d)

#? Using yahoo_fin

def altmanZScore(ticker):
    bs=si.get_balance_sheet(ticker)
    financials=si.get_income_statement(ticker)

    working_capital=bs.loc["totalCurrentAssets"][0] - bs.loc["totalCurrentLiabilities"][0]
    total_assets=bs.loc["totalAssets"][0]
    total_liabilities=bs.loc["totalLiab"][0]
    equity=bs.loc["totalStockholderEquity"][0]
    retained_earnings=bs.loc["retainedEarnings"][0]
    sales=financials.loc["totalRevenue"][0]
    ebit=financials.loc["ebit"][0]

    altman_z= round((1.2 * (working_capital / total_assets) + 1.4 * (retained_earnings / total_assets) + 3.3 * (ebit / total_assets) + 0.6 * (equity / total_liabilities) + 1 * (sales / total_assets)), ndigits=3)

    return altman_z

def netTAV(ticker):
    bs=si.get_balance_sheet(ticker)
    netTangibleAssets = bs.loc["netTangibleAssets"][0]
    
    return separateThousandsbyDots(netTangibleAssets)

def tangibleAssetValue(ticker):
    bs=si.get_balance_sheet(ticker)
    tangibleAssets = bs.loc["netTangibleAssets"][0] + bs.loc["totalLiab"][0]

    return separateThousandsbyDots(tangibleAssets)


#! Math-related functions

def separateThousandsbyDots (num):
    formattedNumber = "{:,}".format(num)
    return formattedNumber.replace(",",".")


if __name__=="__main__":
    print(last4year_balance_sheet("AAPL"))