#!/usr/bin/env python
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose


def data_import():
    #import silver data and extract only price data from it
    silver = pd.read_csv('data/Silver_Futures_Historical_Data.csv', index_col='Date', parse_dates=True)
    silver.sort_index(inplace=True)
    price_silver = silver['Price']

    #import gold data and extract only price data from it
    gold = pd.read_csv('data/Gold_Futures_Historical_Data.csv', index_col='Date', parse_dates=True)
    gold.sort_index(inplace=True)
    price_gold = gold['Price']
    return price_gold, price_silver

def data_clean(price_gold, price_silver, output_path):
    # parse string with a comma thousand separator to number in gold data
    price_gold = price_gold.apply(lambda x: pd.to_numeric(x.replace(',', ''), errors='coerce'))

    # combine gold and silver data and extract weekday data only
    all_weekdays = pd.date_range(start='2019-01-01', end='2019-07-20', freq='B')
    price_silver = price_silver.reindex(all_weekdays)
    price_gold = price_gold.reindex(all_weekdays)

    combined = pd.concat([price_silver, price_gold], axis=1)
    combined.columns=['silver', 'gold']
    combined = combined.dropna(how='any')

    #save the combined file for later use
    fn = output_path + "/" + "combined_data.csv"
    combined.to_csv(fn, sep=",")

    return combined

def data_extraction(df, start, end, type_info):

    interest = df.loc[start:end, type_info]
    return interest

def descriptive_statistics(interest, type_info):
    print(f"The statistics properties of {type_info}:")
    result = interest.describe()
    for key in result.index:
        val = result[key]
        key += ":"
        print(f"{key:8}{val:8.2f}")
    print("\n")


def adf_test(interest, type_info):

    print(f'Augmented Dickey-Fuller Test: {type_info}')
    result = adfuller(interest.dropna(), autolag='AIC')

    labels = ['ADF test statistic', 'p-value', '# lags used', '# observations']
    out = pd.Series(result[0:4], index=labels)

    for key, val in result[4].items():
        out[f'critical value ({key})'] = val

    print(out.to_string())

    if result[1] <= 0.05:
        print("Strong evidence against the null hypothesis")
        print("Reject the null hypothesis")
        print("Data has no unit root and is stationary")
    else:
        print("Weak evidence against the null hypothesis")
        print("Fail to reject the null hypothesis")
        print("Data has a unit root and is non-stationary")
    print("\n")

def ETS_decomposition(interest, type_info, output_path):
    print(f"ETS decomposition analysis for {type_info}:")
    result = seasonal_decompose(interest, model='additive')
    result.plot()
    fn = output_path + "/" + type_info + "_ets_decomposition.pdf"
    plt.savefig(fn)
    print(f'Descriptive statistics of trend composition for {type_info}:')
    trend = result.trend.describe()
    for key in trend.index:
        val = trend[key]
        key += ":"
        print(f"{key:8}{val:8.2f}")

    print(f'Descriptive statistics of seasonal composition for {type_info}:')
    seasonal = result.seasonal.describe()
    for key in seasonal.index:
        val = seasonal[key]
        key += ":"
        print(f"{key:8}{val:8.2f}")

    print(f'Descriptive statistics of error composition for {type_info}:')
    resid = result.resid.describe()
    for key in resid.index:
        val = resid[key]
        key += ":"
        print(f"{key:8}{val:8.2f}")

    print(f'The plot of the ETS decomposition can be found in {fn}.')

if __name__ == "__main__":
    # define command line arguments
    parser = argparse.ArgumentParser(description="Data exploration")
    parser.add_argument("-s", "--start_date", help="in the format of 2017-05-10")
    parser.add_argument("-e", "--end_date", help="in the format of 2017-05-22")
    parser.add_argument("-tp", "--commodity_type", help="either gold or silver")
    args = parser.parse_args()

    # create the output directory if not exists
    output_path = "output"
    os.makedirs(output_path, exist_ok=True)

    # import data
    price_gold, price_silver = data_import()

    # data clean
    combined = data_clean(price_gold, price_silver, output_path)

    # extract data based on specific time period and commodity type
    interest = data_extraction(combined, args.start_date, args.end_date, args.commodity_type)

    # statistical properties
    descriptive_statistics(interest, args.commodity_type)

    # test stationarity
    adf_test(interest, args.commodity_type)

    #error-trend-seasonality decomposition
    ETS_decomposition(interest, args.commodity_type, output_path)













