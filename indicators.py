import yfinance as yf
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


data = yf.download("MSFT",
                   period="1y",
                   interval="1d",
                   progress=False,
                   ignore_tz =True)


data = data.reindex(pd.date_range(start=data.index.min(), end=data.index.max(), freq='D', normalize=True))
data.fillna(method='ffill', inplace=True)

# awesome_osc_data = data.copy()

# awesome_osc_data["Median Price"] = (data["Low"] + data["High"])/2
# awesome_osc_data["5 Median SMA"] = awesome_osc_data["Median Price"].rolling(5).mean()
# awesome_osc_data["34 Median SMA"] =awesome_osc_data["Median Price"].rolling(34).mean()
# awesome_osc_data["Awesome Osc."] = awesome_osc_data["5 Median SMA"] - awesome_osc_data["34 Median SMA"]
# awesome_osc_data["Awesome Diff"] = awesome_osc_data["Awesome Osc."] - awesome_osc_data["Awesome Osc."].shift()

# awesome_osc_data["Awesome Color"] = awesome_osc_data["Awesome Diff"].apply(lambda x: "green" if x>0 else "red" if x<0 else "gray")
# awesome_osc_data=awesome_osc_data.dropna()

# fig1 = make_subplots(rows=2, cols=1, row_heights = [0.7, 0.3], vertical_spacing=0.10, subplot_titles=["MSFT Stock Price", "Awesome Oscillator"], shared_xaxes=True)

# fig1.add_trace(go.Scatter(x=awesome_osc_data.index, y=awesome_osc_data["Adj Close"], showlegend=False), col=1, row=1)
# fig1.add_trace(go.Bar(x=awesome_osc_data.index, y=awesome_osc_data["Awesome Osc."], marker_color = awesome_osc_data["Awesome Color"], showlegend=False), col=1, row=2)

# fig1.update_layout(height=600, width=1000)
# fig1.show()

atr_data = data.copy()

atr_data["H-L"] = atr_data["High"] - atr_data["Low"]
atr_data["H-Cp"] = abs(atr_data["High"] - atr_data["Adj Close"].shift())
atr_data["L-Cp"] = abs(atr_data["Low"]- atr_data["Adj Close"].shift())

atr_data["True Range"] = atr_data[["H-L", "H-Cp", "L-Cp"]].max(axis=1)
atr_data["ATR-14"] = atr_data["True Range"].rolling(14).mean()

atr_data = atr_data.dropna()

fig2 = make_subplots(rows=2, cols=1, row_heights = [0.7, 0.3], vertical_spacing=0.10, subplot_titles=["MSFT Stock Price", "Average True Range"], shared_xaxes=True)

fig2.add_trace(go.Scatter(x=atr_data.index, y=atr_data["Adj Close"], showlegend=False), col=1, row=1)
fig2.add_trace(go.Scatter(x=atr_data.index, y=atr_data["ATR-14"], marker_color = "red", showlegend=False), col=1, row=2)

fig2.update_layout(height=700, width=1500)
fig2.show()