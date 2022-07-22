# from pandas import read_csv
# from statsmodels.graphics.tsaplots import plot_acf
# from statsmodels.graphics.tsaplots import plot_pacf
# from pandas.plotting import autocorrelation_plot
# from matplotlib import pyplot
# import numpy as np

# series=read_csv('./Src/trend.csv',header=None,index_col=None)
# series_log=np.log(series)


##########################
# ACF PACF Plots
##########################

# pyplot.plot(series_log)
# pyplot.show()

# plot_acf(series_log,lags=150)
# pyplot.show()

# plot_pacf(series.values)
# pyplot.show()

# autocorrelation_plot(series.values)
# pyplot.show()

# ARIMA Model fitting


from pickle import NONE
import warnings
from pandas import read_csv
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt

###########################################################

# ARIMA evaluation for given order (p,d,q) and return RMSE

def evaluate_arima(X,Aorder):
    X=X.astype('float64')
    train_data_size=int(0.75*(len(X)))
    train_data=X[:train_data_size]
    test_data=X[train_data_size:]
    history=[x for x in train_data]
    predictions=list()
    for i in range(len(test_data)):
        model=ARIMA(history,order=Aorder)
        model_fit=model.fit()
        predicted_val=model_fit.forecast()[0]
        predictions.append(predicted_val)
        history.append(test_data[i])
    RMSE=sqrt(mean_squared_error(test_data,predictions))
    return RMSE

############################################################

def evaluate_possible_models(data,p_list,d_list,q_list):
    min_rmse=float("inf")
    best_order=None
    for p in p_list:
        for q in q_list:
            for d in d_list:
                order=(p,d,q)
                try:
                    rmse=evaluate_arima(data,order)
                    if rmse<min_rmse:
                        min_rmse=rmse
                        best_order=order
                    print('ARIMA%s RMSE=%.3f' % (order,rmse))
                except:
                    print("Some exception")
                    continue
                    
    print('Best ARIMA%s RMSE=%.3f' % (best_order,min_rmse))

series = read_csv('./Src/trend.csv', header=None, index_col=None)

P=range(0,8)
D=range(1,3)
Q=range(2,3)

warnings.filterwarnings("ignore")
X=series.values
evaluate_possible_models(X,P,D,Q)

