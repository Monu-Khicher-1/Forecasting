from pandas import read_csv
from pandas import Series
from statsmodels.tsa.stattools import adfuller
from matplotlib import pyplot

# create a differenced time series
def difference(dataset):
    diff = list()
    for i in range(1, len(dataset)):
        value = dataset[i] - dataset[i - 1]
        diff.append(value)
    return Series(diff)

# Reading Data
series=read_csv('../Src/electricity_data.csv',header=0,index_col=None,parse_dates=True,squeeze=True)


X=series.MCP

print(X)


# applying difference d=1
diff1=difference(X)
diff1.index=series.index[1:]

print("Hello")
# applying adfuller test
result=adfuller(diff1)

# Result of add fuller test
print("--------------------------------------------------------------")
print("- For d=1")
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))


diff1.to_csv('../Files/diff1.csv',header=False)
diff1.plot()
pyplot.show()

# applying d=2

diff2=difference(diff1.values)
diff2.index=diff1.index[1:]

# applying adfuller test
result=adfuller(diff2)

# Result of add fuller test
print("--------------------------------------------------------------")
print("- For d=2")
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))


diff2.to_csv('../Files/diff2.csv',header=False)
diff2.plot()
pyplot.show()
