#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima
from statsmodels.graphics.tsaplots import plot_acf

def model_selection(df, type_info):
    print(f'the selected model for {type_info}')
    stepwise_fit = auto_arima(df, start_p=0, start_q=0,
                                   max_p=2, max_q=2, m=12,
                                   seasonal=False,
                                   d=None, trace=True,
                                   error_action='ignore',  # we don't want to know if an order does not work
                                   suppress_warnings=True,  # we don't want convergence warnings
                                   stepwise=True)  # set to stepwise
    print(stepwise_fit.summary())
    print('\n')

def acf_plot(df, type_info, fn):
    diff = df - df.shift(1)
    diff = diff.dropna()
    title = f'Autocorrelation: {type_info}'
    plot_acf(diff, title=title);
    plt.savefig(fn)

if __name__ == "__main__":

    # data import:
    df = pd.read_csv('output/combined_data.csv', sep=',')

    # extract gold and silver from data
    silver, gold = df['silver'], df['gold']

    # model selection
    model_selection(silver, "silver")
    model_selection(gold, "gold")

    # ACF plot
    silver_fn = 'output/silver_acf.pdf'
    gold_fn = 'output/gold_acf.pdf'
    acf_plot(silver, "silver", silver_fn)
    acf_plot(gold, "gold", gold_fn)

