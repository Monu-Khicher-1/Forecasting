# Introduction

# ARIMA Model
 An autoregressive integrated moving average, or ARIMA, is a statistical analysis model that uses time series data to either better understand the data set or to predict future trends. 
 * **Autoregression (AR):** refers to a model that shows a changing variable that regresses on its own lagged, or prior, values.
 * **Integrated (I):** represents the differencing of raw observations to allow for the time series to become stationary (i.e., data values are replaced by the difference between the data values and the previous values).
* **Moving average (MA):**  incorporates the dependency between an observation and a residual error from a moving average model applied to lagged observations.

## Setup
It requiers following libraries:
* Pandas
* Matplotlib
* statsmodels

## Identification
Actual Data of Electricity MCP is non-stationary. For making it stationary we can use different methods.

Plot of actual data:
![Electricity Data Plot](/Img/Electricity_data_MCP_Plot.png)

### Transform Data
Data transforms are intended to remove noise and improve the signal in time series forecasting.
Some Data transform methods:
-  **Square Root Transform:** A time series that has a quadratic growth trend can be made linear by taking the square root.
- **Log Transform:** Time series with an exponential distribution can be made linear by taking the logarithm of the values. This is called a log transform. 
- **Box-Cox-Transform:** This transform is combination of both Log and Square Root Trasform. 
Box–Cox transformation is defined as:
![Box-Cox-Transform Formula](/Img/box-cox-transform.png)

Below are some common values for lambda:
* lambda = -1.0 is a reciprocal transform.
* lambda = -0.5 is a reciprocal square root transform.
* lambda = 0.0 is a log transform.
* lambda = 0.5 is a square root transform.
* lambda = 1.0 is no transform.

After applying Box-cox Transformation to the data:
![Transformed Data Plot](/Img/Electricity_data_box_cox_transformed.png)
For variance stablization Lambda= -0.203252 is suitable. (python code for this are: /Model/box_cox_transfor.py)

### Data Stationarty

For stationarizing data we can use nth order differencing. Higher Order Difference is not preferable.

* **1st order differenced data:** After first order difference we get following data plot:
![1st Order Difference](/Img/Electricity_data_adf_diff1.png)

* **2nd order differenced data:** After first order difference we get following data plot:
![2nd Order Difference](/Img/Electricity_data_adf_diff2.png)

### ADF Test 
ADF Test Results for 1st order and 2nd order dierenced data:
![ADF Test Result](/Img/Electricity_data_adf.png)

**Data is stationary for d=1 as well as for d=2.**
So, d = 1 .

## Estimation


### Parameter Selection
ARIMA model has 3 parameters p,d,q. d had been calculated above.

* **For parameter p:** Autocorelation plot is used for p-values. Autocorelation plot for electricity data is:

![Autocorelation plot](/Img/Electricity_data_autocorrelation.png)

More clear Image:

![Autocorelation plot](/Img/Electricity_data_acf_lag50.png)

* **For parameter q:** Partial Autocorelation plot is used for q-values. Partial Autocorelation plot for electricity data is:

![Partial Autocorelation plot](/Img/Electricity_data_pacf.png)

Clearly q=2. 

### Best Model Selection

## Diagnostic

## Forecasting
 Results for ARIMA(2,1,2) are as following:
 ![1-Jan-2021-Test-Table](/Img/Electricity_data_arima_2_1_2_predictions_2021_1_1.png)
 Graph:
 ![1-Jan-2021-Test-Graph](/Img/Electricity_data_arima_2_1_2_preditions.png)
 Details of Model ARIMA(2,1,2):
 ![Summary ARIMA(2,1,2)](/Img/Electricity_data_arima_2_1_2_arima_summary.png)








