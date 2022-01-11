import numpy as np
import pandas_datareader as pdr
import datetime as dt 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from dateutil import relativedelta as rd
import statsmodels.api as sm


def riskFreeRate():
    riskf = pdr.get_data_yahoo("^TNX")
    rates = riskf["Adj Close"]
    return round(rates[-1]/100, 8)





def beta_rolling(tickers, start_date, end_date, window):
    new_tickers = tickers
    new_tickers.append("^GSPC")

    data = pdr.get_data_yahoo(new_tickers, start_date, end_date, interval="m")
    data = data["Adj Close"]

    log_returns = np.log(data/data.shift())
    df_log_returns = pd.DataFrame(log_returns)

    betas = pd.DataFrame()
    
    for i in tickers:
        ticker_ret = df_log_returns[i]
        market_ret = df_log_returns["^GSPC"]
        betas[f"{i} Beta"] = ticker_ret.rolling(window).cov() / market_ret.rolling(window).var()

    del betas["^GSPC Beta"]

    fig, ax = plt.subplots()
    plt.plot(betas, label=betas.columns)
    ax.legend()
    ax.set(title="Rolling Beta", xlabel="Date", ylabel="Beta")
    
    return fig



def correlation(tickers, start_date, end_date):
    new_tickers = tickers
    new_tickers.append("^GSPC")
    
    data = pdr.get_data_yahoo(tickers, start_date, end_date, interval="m")
    data = data["Adj Close"]
    
    log_returns = np.log(data/data.shift())
    correlation = log_returns.corr()
    correlation.rename(columns={"^GSPC":"S&P500"})

    fig, ax = plt.subplots()
    sns.heatmap(correlation, annot=True)
    ax.set(title="Correlation Matrix", xlabel="Tickers", ylabel="Tickers")

    return fig

def log_rets(tickers, start_date, end_date):
    data = pdr.get_data_yahoo(tickers, start_date, end_date, interval="m")
    data = data["Adj Close"]
    
   

    log_returns = np.log(data/data.shift())
    return log_returns

def efficientFrontier(tickers, start_date, end_date):

    data = pdr.get_data_yahoo(tickers, start_date, end_date, interval="m")
    data = data["Adj Close"]

    log_returns = np.log(data/data.shift())

    weight = np.random.random(len(tickers))
    weight /= weight.sum()

    #exp_return = np.sum(log_returns.mean()* weight)*252

    #exp_vol = np.sqrt(np.dot(weight, np.dot(log_returns.cov()*252,weight)))

    rf = riskFreeRate()

    n = 5000 #runs
    weights = np.zeros((n,len(tickers)))
    exp_rtns = np.zeros(n)
    exp_vols = np.zeros(n)
    sharpe_ratios = np.zeros(n)

    for i in range(n):
        weight = np.random.random(len(tickers))
        weight /= weight.sum()
        weights[i] = weight

        exp_rtns[i] = np.sum(log_returns.mean()*weight)*252
        exp_vols[i] = np.sqrt(np.dot(weight, np.dot(log_returns.cov()*252,weight)))
        sharpe_ratios[i] = (exp_rtns[i]-rf)/exp_vols[i]

    fig,ax = plt.subplots()

    main = ax.scatter(exp_vols,exp_rtns, c=sharpe_ratios)
    ax.scatter(exp_vols[sharpe_ratios.argmax()], exp_rtns[sharpe_ratios.argmax()], c="red", label="Highest Sharpe Ratio Portfolio")
    ax.scatter(exp_vols[exp_vols.argmin()], exp_rtns[exp_vols.argmin()], c="orange", label="Minimum Risk Portfolio")
    ax.legend()
    #ax.set_ylim(0)
    ax.set(title="Efficient Frontier")
    ax.set_xlabel("Expected Volatility")
    ax.set_ylabel("Expected Return")
    fig.colorbar(main, label="Sharpe Ratio")

    return fig
 
def beta(tickers, start_date, end_date):
    new_tickers = tickers
    new_tickers.append("^GSPC")

    data = pdr.get_data_yahoo(new_tickers, start_date, end_date, interval="m")
    data = data["Adj Close"]

    log_returns = pd.DataFrame(np.log(data/data.shift()))
    
    cov = log_returns.cov()
    var = log_returns["^GSPC"].var()

    beta_values = cov.loc["^GSPC"]/var
    
    beta_table = beta_values.to_frame("Beta")["Beta"]
    beta_table.rename({"^GSPC":"S&P500"}, inplace=True)
    
    return beta_table


st.set_page_config(layout="wide")

ticker_input = st.sidebar.text_input("Enter the tickers space-separated")
tickers = ticker_input.strip()
tickers = tickers.split(" ")
start_date = st.sidebar.date_input('Start date (format=DD/MM/YYYY)', min_value=dt.datetime(1950,1,1))
end_date = st.sidebar.date_input('End date (format=DD/MM/YYYY)', max_value=dt.datetime.today())
month_delta = rd.relativedelta(end_date,start_date).years * 12
beta_window = st.sidebar.slider("Rolling Beta Window", 1, int(month_delta/4))
run_button = st.sidebar.button("Run calculations")

# Conflict between Beta Function and Efficient Frontier

with st.spinner(text='In progress'):
    if run_button:
        if start_date < end_date:
            st.sidebar.success('Start date: `%s`\n\nEnd date: `%s`' % (start_date, end_date))
            st.header("Financial Analysis Toolkit")
            st.subheader("Made by Tiago Moreira")
            st.subheader("Correlation between chosen stocks and the market")
            st.pyplot(correlation(tickers, start_date, end_date))
            st.subheader("Efficient Frontier")
            st.pyplot(efficientFrontier(tickers, start_date, end_date))  #add capital market line radio button
            st.subheader("Overall Beta")
            st.dataframe(beta(tickers, start_date, end_date))
            st.subheader("Rolling Beta")
            st.pyplot(beta_rolling(tickers,start_date, end_date, beta_window))
            st.write("Beware: Rolling window starts on the date of the latest of the stocks to enter the market.")
            #st.dataframe(log_rets(tickers, start_date, end_date))
        else:
            st.sidebar.error('Error: End date must fall after start date.')