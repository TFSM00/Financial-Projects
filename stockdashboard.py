import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=AAPL&apikey=S53UKPY4QRGST5HW'
r = requests.get(url)
data = r.json()
newd = data.get("annualReports")
new = pd.DataFrame(newd).T
#new.set_index("fiscalDateEnding")
st.dataframe(new)
#st.write(len(new))