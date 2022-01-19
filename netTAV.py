
#! From "Intelligent Investor" by Benjamin Graham

#? Tangible Assets = Total Assets - Intangible Assets
#? Net Tangible Assets = Total Assets - Intangible Assets - Total Liabilities

import yahoo_fin.stock_info as si  #* imports fundamentals package
import pandas as pd
import stockfunctions as sf
from sys import argv

#* CMD ARGUMENT CHECK
try:
    ticker = argv[1]
    if ticker == "help":
        print("Correct use of the command: netTAV.py [ticker]\n\nA company with high NTA is able to obtain acquisition financing more easily since it owns more assets to use as security for loans.\n\nNTA can be used to determine company risk levels such as solvency and liquidity.\n\nIt is important to know that although determining the NTA for a company offers benefits, its usefulness varies greatly across industries.\n\nFor example, medical device manufacturers often own intangible assets (patents) that are far more valuable than their tangible assets. On the other hand, real estate holding companies own little to no intangible assets")
        quit()
except IndexError: #*if no argument give help and quit
    print("Wrong use of the command. Do netTAV.py [ticker]")
    quit()

#* VALID TICKER CHECK
try:
    bs=si.get_balance_sheet(ticker)
except TypeError:
    print("Ticker is invalid")
    quit()


tangibleAssets = bs.loc["netTangibleAssets"][0] + bs.loc["totalLiab"][0]
netTangibleAssets = bs.loc["netTangibleAssets"][0]

info = sf.stockinfo(ticker) 
name = info["shortName"]
currency = info["currency"]

print("Tangible Assets for " + name + ": " + sf.separateThousandsbyDots(tangibleAssets) + " " + currency)
print("Net Tangible Assets for " + name + ": " + sf.separateThousandsbyDots(netTangibleAssets) + " " + currency)