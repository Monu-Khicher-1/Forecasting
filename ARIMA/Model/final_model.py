from pandas import read_csv
from pandas import DataFrame
from statsmodels.tsa.arima.model import ARIMA
from matplotlib import pyplot
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from sklearn.metrics import mean_squared_error
from math import sqrt



series1=read_csv('../Src/electricity_data.csv',header=0,index_col=0,parse_dates=True,squeeze=True)
series2=read_csv('../Src/test_data.csv',header=0,index_col=0,parse_dates=True,squeeze=True)

X = series1.MCP.values
X = X.astype('float64')
Y=series2.MCP.values
Y=Y.astype('float64')

train=X
test=Y

history = [x for x in train]
predictions = list()
for i in range(len(test)):
    model = ARIMA(history, order=(2,1,2))
    model_fit = model.fit()
    yhat = model_fit.forecast()[0]
    predictions.append(yhat)
    # observation
    obs = test[i]
    history.append(obs)
    print('>Predicted=%.3f, Expected=%.3f' % (yhat, obs))
# errors
rmse = sqrt(mean_squared_error(test, predictions))
print('RMSE: %.3f' % rmse)

pyplot.plot(train[len(train)-50:])
pyplot.plot([None for x in range(49)]+[train[(len(train)-1)]]+[x for x in predictions],color='red')
pyplot.plot([None for x in range(49)]+[train[(len(train)-1)]]+[x for x in test],color='green')
pyplot.show()

# residuals = [test[i]-predictions[i] for i in range(len(test))]
# residuals = DataFrame(residuals)

# plot_pacf(residuals)
# pyplot.show()

# plot_acf(residuals)
# pyplot.show()

# pyplot.figure()
# pyplot.subplot(211)
# residuals.hist(ax=pyplot.gca())
# pyplot.subplot(212)
# residuals.plot(kind='kde', ax=pyplot.gca())
# pyplot.show()


