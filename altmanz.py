import yahoo_fin.stock_info as si  #* imports fundamentals package
import pandas as pd
import stockfunctions as sf
from sys import argv #* lets me check for arguments in the cmd

#! Altman Z-Score = 

#! 1.2*(working capital / total assets) bl sheet 4 years
#! 1.4*(retained earnings / total assets) bl sheet 4 years
#! 3.3*(earnings before interest and tax / total assets) financials
#! 0.6*(market value of equity / total liabilities) bl sheet 4 years
#! 1.0*(sales / total assets) earnings

#? working capital = current assets - current liabilities

try:
    ticker = argv[1] #*checks for cmd argument
except IndexError: #*if no argument give help and quit
    print("Wrong use of the command. Do altmanz.py [ticker]")
    quit()

try: #*checks if the ticker is valid
    bs=si.get_balance_sheet(ticker)
    financials=si.get_income_statement(ticker)
except TypeError:
    print("Ticker is invalid")
    quit()

working_capital=bs.loc["totalCurrentAssets"][0] - bs.loc["totalCurrentLiabilities"][0]
total_assets=bs.loc["totalAssets"][0]
total_liabilities=bs.loc["totalLiab"][0]
equity=bs.loc["totalStockholderEquity"][0]
retained_earnings=bs.loc["retainedEarnings"][0]
sales=financials.loc["totalRevenue"][0]
ebit=financials.loc["ebit"][0]

info = sf.stockinfo(ticker) 
name = info["shortName"]

altman_z= round((1.2 * (working_capital / total_assets) + 1.4 * (retained_earnings / total_assets) + 3.3 * (ebit / total_assets) + 0.6 * (equity / total_liabilities) + 1 * (sales / total_assets)), ndigits=3)


#*makes the altman z score conditions and reports the company's chance of bankruptcy
if altman_z <= 1.8:
    print("Altman Z-Score for " + name + " = " + str(altman_z))
    print(name + " has a high probability of bankruptcy in the next 2 years.")
elif altman_z > 1.8 and altman_z <= 3:
    print("Altman Z-Score for " + name + " = " + str(altman_z))
    print(name + " has a moderate probability of bankruptcy in the next 2 years.")
elif altman_z > 3:
    print("Altman Z-Score for " + name + " = " + str(altman_z))
    print(name + " has a low probability of bankruptcy in the next 2 years")
else:
    print("Altman Z-Score for " + name + " = " + str(altman_z))
    print("Something went wrong: the score is invalid (less than zero)")
    logfile = open("altman_z_error", "a") #*makes log file if the score is invalid to check the company used
    logfile.write(ticker + ": Score of " + str(altman_z))

