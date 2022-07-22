from pandas import read_csv
from sklearn.metrics import mean_squared_error
from math import sqrt
from statsmodels.tsa.arima.model import ARIMA
from matplotlib import pyplot
import numpy
import warnings

warnings.filterwarnings("ignore")

data=read_csv('./Src/data.csv',header=None,index_col=None)
trend=read_csv('./Src/trend.csv',header=None,index_col=None)
residual=read_csv('./Src/residual_error(A).csv',header=None,index_col=None)
seasonality=numpy.load('seasonality.npy')
print(seasonality)

X = trend.values
X = X.astype('float64')

Y = residual.values
Y = Y.astype('float64')

Z=data.values
Z=Z.astype('float64')

train_trend1=X[:int(0.80*len(X))]
train_trend=[float(x) for x in train_trend1]
test_trend1=Z[len(Z)-(int(len(X))-int(0.80*len(X))):]
test_trend=[float(x) for x in test_trend1]
train_residual=Y

history_residual = [float(x) for x in train_residual]
history_trend = [float(x) for x in train_trend]
for k in range(1):
    for j in range(1):
        predictions_trend = list()
        predictions_residual = list()
        predictions_trend_plus_seasonality=list()
        predictions_net=list()
        # n=int(input("Range: "))
        n=len(test_trend)


        for i in range(n):
            model = ARIMA(history_trend, order=(7,1,2))
            model_fit = model.fit()
            trend_pre = model_fit.forecast()[0]
            model2 = ARIMA(history_residual, order=(3,0,2))
            model2_fit = model2.fit()
            residual_pre = model2_fit.forecast()[0]
            predictions_trend.append(trend_pre)
            predictions_trend_plus_seasonality.append(trend_pre+seasonality[(i+len(train_trend))%12]+residual_pre)
            predictions_residual.append(residual_pre)
            history_residual.append(residual_pre)

            # observation
            history_trend.append(trend_pre)
            print(' %.3f ,  %.3f' % (predictions_trend_plus_seasonality[i],test_trend[i]))
            # print('>Predicted Orignal %d = %.3f' % (i,trend_pre))
        # errors
        RMSE=sqrt(mean_squared_error(test_trend,predictions_trend_plus_seasonality))
        print("RMSE: ", RMSE)

        print(">Trend ARIMA(%d,1,2) & Residual ARIMA(%d,0,2)|| RMSE: %.3f " % (j,k,RMSE))
        # print("Residuals:",predictions_residual)
        # print("Trend:",predictions_trend_plus_seasonality)



        pyplot.plot(data)
        pyplot.plot([None for x in range(12)]+[x for x in train_trend],color='red')
        pyplot.plot([None for x in range(12+len(train_trend))]+[train_trend[(len(train_trend)-1)]]+[x for x in predictions_trend],color='red')
        pyplot.plot([None for x in range(12+len(train_trend))]+[train_trend[(len(train_trend)-1)]]+[x for x in predictions_trend_plus_seasonality],color='green')
        pyplot.show()
