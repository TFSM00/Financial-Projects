import getFamaFrenchFactors as gff
import pandas as pd
import datetime as dt

ff3 = gff.famaFrench3Factor(frequency="m")
ff3 = ff3.set_index("date_ff_factors")

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

start_date = dt.datetime(2004,1,1)
end_date = dt.datetime(2022,1,26)
#print(ff3["date_ff_factors"])

index = ff3.index.tolist()

near_st = nearest(index, start_date)
near_end = nearest(index, end_date)
#print(ff3["date_ff_factors"].loc[near_st])

start_ind = index.index(near_st)
end_ind = index.index(near_end) + 1

rfs = ff3["RF"][start_ind: end_ind]
print(rfs.mean())
