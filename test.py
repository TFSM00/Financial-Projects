import pandas as pd
import numpy as np
import pandas_datareader as pdr
import datetime as dt
import streamlit as st

tickers = ["AAPL", "TWTR", "IBM", "MSFT", "^GSPC"]
start = dt.datetime(1999, 1, 1)
data = pdr.get_data_yahoo(tickers, start)
data = data["Adj Close"]

log_returns = np.log(data / data.shift())

st.dataframe(log_returns)