import yfinance as yf

import pandas as pd
import matplotlib.pyplot as plt

data = yf.download("MSFT",
                   period="5d",
                   interval="1m",
                   progress=False) #non-verbose

data["Median Price"] = (data["Low"] + data["High"])/2
data["5 Median SMA"] = data["Median Price"].rolling(5).mean()
data["34 Median SMA"] = data["Median Price"].rolling(34).mean()
data["Awesome Osc."] = data["5 Median SMA"] - data["34 Median SMA"]

fig, axs = plt.subplots(2, 1)
axs[0].plot(data["Adj Close"])
axs[1].plot(data["Awesome Osc."])

plt.show()
print(data)