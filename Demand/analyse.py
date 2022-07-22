from pandas import read_csv
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
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

train_size=int(len(X)*0.80)

train_trend=X[:train_size]
train_residual=Y[:train_size]

history_residual = [float(x) for x in train_residual]
history_trend = [float(x) for x in train_trend]


test_trend1=X[train_size:]
test_residual1=Y[train_size:]

test_trend=[float(x) for x in test_trend1]
test_residual=[float(x) for x in test_residual1]



predictions_trend = list()
predictions_residual = list()
predictions_trend_plus_seasonality=list()
predictions_net=list()

for i in range(len(test_trend)):
    model = ARIMA(history_trend, order=(136,1,2))
    model_fit = model.fit()
    trend_pre = model_fit.forecast()[0]
    model2 = ARIMA(history_residual, order=(4,0,2))
    model2_fit = model2.fit()
    residual_pre = model2_fit.forecast()[0]
    predictions_trend.append(trend_pre)

    pre=trend_pre+seasonality[(i+train_size)%12]+residual_pre
    predictions_trend_plus_seasonality.append(pre)
    predictions_residual.append(residual_pre)
    history_residual.append(test_residual[i])

    # observation
    history_trend.append(test_trend[i])
    print('>Predicted Trend %d = %.3f' % (i,pre))
    # print('>Predicted Orignal %d = %.3f' % (i,trend_pre))
# errors
test_data=data[train_size:train_size+len(test_trend)]

RMSE=sqrt(mean_squared_error(test_data,predictions_trend_plus_seasonality))
print("RMSE :",RMSE)

print("Residuals:",predictions_residual)
print("Trend:",predictions_trend_plus_seasonality)

pyplot.plot(data)
pyplot.plot([None for x in range(12)]+[x for x in train_trend],color='red')
pyplot.plot([None for x in range(12+len(train_trend))]+[train_trend[(len(train_trend)-1)]]+[x for x in predictions_trend],color='red')
pyplot.plot([None for x in range(12+len(train_trend))]+[train_trend[(len(train_trend)-1)]]+[x for x in predictions_trend_plus_seasonality],color='green')
pyplot.show()
