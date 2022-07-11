from pickle import NONE
import warnings
from pandas import read_csv
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from scipy.stats import boxcox
from math import sqrt
from math import log
from math import exp

##################################################

# ARIMA evaluation for given order (p,d,q) and return RMSE

def boxcox_inverse(value, lam):
    if lam == 0:
       return exp(value)
    return exp(log(lam * value + 1) / lam)


def evaluate_arima(X,Aorder):
    X=X.astype('float64')
    train_data_size=int(len(X)*0.9995)
    train_data , test_data=X[0:train_data_size], X[train_data_size:]
    history=[x for x in train_data]
    predictions=list()
    print("----------------------------")
    for i in range(len(test_data)):
        transformed, lam = boxcox(history)
        if lam < -5:
            transformed, lam = history, 1
        model=ARIMA(transformed,order=Aorder)
        model_fit=model.fit()
        predicted_val=model_fit.forecast()[0]
        predicted_val=boxcox_inverse(predicted_val,lam)
        predictions.append(predicted_val)
        history.append(test_data[i])
        print('>Predicted=%.3f, Expected=%.3f' % (predicted_val, test_data[i]))
    RMSE=sqrt(mean_squared_error(test_data,predictions))
    return RMSE
    
###################################################

def evaluate_possible_models(data,p_list,d_list,q_list):
    data=data.astype('float64')
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
                    print("Some Error occured.")
                    continue
                 
    print('Best ARIMA%s RMSE=%.3f' % (best_order,min_rmse))

series=read_csv('../Src/electricity_data.csv',header=0,index_col=0,parse_dates=True,squeeze=True)

P=range(0,4)
D=range(1,2)
Q=range(1,3)

warnings.filterwarnings("ignore")
X=series.MCP.values
evaluate_possible_models(X, P,D,Q)
