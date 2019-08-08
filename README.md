## Answer:

### Step 1

- Save the gold and silver historical data as csv files in folder data/. Folder Data/ and two programs should be in the same folder for running.

### Step 2

- `data_exploration.py` is responsible for step 2. The template command used to run the program should be:

  `python data_exploration.py -s ‘2019-01-01’ -e ‘2019-07-20’ -tp ‘gold’`

  All the results will be directly printed out on the screen while a plot will be generated in the folder output/.

- I first imported data and extract price and weekday data for silver and gold, for this make more sense when we analyze the trade data. I also saved the extracted data name as `combined_data.csv` in folder output/ for step 3.

- I then extracted gold data with the time period 2019-01-01 to 2019-07-19 as required command line arguments.

- For the statistical properties, as listed below, I inculded the mean, std, min, max and also 25%, 50%, 75% quantile for the data.

  ```python
  count     144.000000
  mean     1321.727083
  std        43.563037
  min      1272.000000
  25%      1293.175000
  50%      1307.700000
  75%      1331.675000
  max      1444.250000
  ```

   

- To test stationarity, I used Augmented Dickey-Fuller Test and reported non-staionary for the p-vale > 0.05.

  ```bash
  Augmented Dickey-Fuller Test: Gold
  ADF test statistic       -0.076146
  p-value                   0.951763
  # lags used               1.000000
  # observations          142.000000
  critical value (1%)      -3.477262
  critical value (5%)      -2.882118
  critical value (10%)     -2.577743
  Weak evidence against the null hypothesis
  Fail to reject the null hypothesis
  Data has a unit root and is non-stationary
  ```

- To show other properties of time-series data, I did an ETS Decomposition. The descriptive statistics of trend, seasonal and residual are shown below and I also saved the plot as `gold_ets_decomposition.pdf` in folder output/. As shown below, we can see from the plot that the data is non-stationary, has trend and non-seasonal.

  ```bash
  ETS decomposition analysis for gold:
  Descriptive statistics of trend composition for gold:
  count:    140.00
  mean:    1320.58
  std:       41.10
  min:     1276.30
  25%:     1294.32
  50%:     1305.45
  75%:     1331.80
  max:     1424.06
  Descriptive statistics of seasonal composition for gold:
  count:    144.00
  mean:       0.01
  std:        0.88
  min:       -1.34
  25%:       -0.49
  50%:       -0.01
  75%:        0.65
  max:        1.19
  Descriptive statistics of error composition for gold:
  count:    140.00
  mean:      -0.03
  std:        6.30
  min:      -24.32
  25%:       -3.57
  50%:       -0.17
  75%:        3.33
  max:       18.32
  ```

  ![gold_est_decomposition](/Users/qizhihua/Desktop/gold_est_decomposition.png)

### Step 3

- `model_selection.py`  is responsible for step 2. The template command used to run the program should be:

  ​	`python model_selection.py`

  All the results will be directly printed out on the screen while two plots will be generated in the folder output/.

- I first imported the `combined_data.csv` which was generated in step 2 including gold and silver data from Jan 2019 till now.

- For gold and silver, I both ran autoarima which will select best model based on AIC. As show below, the best model for gold is ARIMA(1, 1, 1) and the best model for silver is ARIMA( 0, 1, 0).

```bash
The selected model for silver
Fit ARIMA: order=(0, 1, 0); AIC=-110.709, BIC=-104.783, Fit time=0.009 seconds
Fit ARIMA: order=(1, 1, 0); AIC=-110.568, BIC=-101.680, Fit time=0.020 seconds
Fit ARIMA: order=(0, 1, 1); AIC=-110.317, BIC=-101.428, Fit time=0.025 seconds
Fit ARIMA: order=(1, 1, 1); AIC=-108.893, BIC=-97.042, Fit time=0.097 seconds
Total fit time: 0.154 seconds
                             ARIMA Model Results
==============================================================================
Dep. Variable:                    D.y   No. Observations:                  143
Model:                 ARIMA(0, 1, 0)   Log Likelihood                  57.354
Method:                           css   S.D. of innovations              0.162
Date:                Sun, 21 Jul 2019   AIC                           -110.709
Time:                        23:39:51   BIC                           -104.783
Sample:                             1   HQIC                          -108.301

==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
const          0.0047      0.014      0.347      0.729      -0.022       0.031
==============================================================================
```

```bash
The selected model for gold
Fit ARIMA: order=(0, 1, 0); AIC=1086.288, BIC=1092.214, Fit time=0.002 seconds
Fit ARIMA: order=(1, 1, 0); AIC=1084.371, BIC=1093.259, Fit time=0.012 seconds
Fit ARIMA: order=(0, 1, 1); AIC=1084.911, BIC=1093.800, Fit time=0.018 seconds
Fit ARIMA: order=(2, 1, 0); AIC=1085.663, BIC=1097.515, Fit time=0.034 seconds
Fit ARIMA: order=(1, 1, 1); AIC=1083.742, BIC=1095.594, Fit time=0.105 seconds
Fit ARIMA: order=(2, 1, 2); AIC=1089.591, BIC=1107.368, Fit time=0.189 seconds
Fit ARIMA: order=(2, 1, 1); AIC=1084.925, BIC=1099.739, Fit time=0.078 seconds
Fit ARIMA: order=(1, 1, 2); AIC=1087.585, BIC=1102.399, Fit time=0.078 seconds
Total fit time: 0.517 seconds
                             ARIMA Model Results
==============================================================================
Dep. Variable:                    D.y   No. Observations:                  143
Model:                 ARIMA(1, 1, 1)   Log Likelihood                -537.871
Method:                       css-mle   S.D. of innovations             10.397
Date:                Sun, 21 Jul 2019   AIC                           1083.742
Time:                        23:39:52   BIC                           1095.594
Sample:                             1   HQIC                          1088.558

==============================================================================
                 coef    std err          z      P>|z|      [0.025      0.975]
------------------------------------------------------------------------------
const          1.0195      0.841      1.213      0.227      -0.628       2.667
ar.L1.D.y     -0.9632      0.058    -16.718      0.000      -1.076      -0.850
ma.L1.D.y      0.8982      0.085     10.509      0.000       0.731       1.066
                                    Roots
=============================================================================
                  Real          Imaginary           Modulus         Frequency
-----------------------------------------------------------------------------
AR.1           -1.0382           +0.0000j            1.0382            0.5000
MA.1           -1.1133           +0.0000j            1.1133            0.5000
-----------------------------------------------------------------------------
```

- I futher did ACF-plot to check the autocorrelation on gold's and silver's diffenece. These two plots were saved in folder output/.

   ![silver_acf](/Users/qizhihua/Desktop/silver_acf.png)

  ![gold_acf](/Users/qizhihua/Desktop/gold_acf.png)

- The best model for silver price is ARIMA (0, 1, 0), so the best model for silver price direction of change will be ARIMA (0, 0, 0). These represent random walk model and white noise model respectively. And the ACF plot can confirm this result. For gold price, the best model is ARIMA (1, 1, 1), so the best model for gold price direction of change will be ARMA (1,1). But this choice is based on AIC, as we can see from the step-wise detail, ARIMA (0,1,0) has the lowest BIC and the difference between AIC is quite small. Combined with the ACF plot, past prices are not useful in predicting future prices or direction of change. Applying random walk and white noise model to data suggests that commodity prices and direction change randomly, and it is not possible to beat or predict the market because prices reflect all available information and the occurrence of new information is seemingly random as well.