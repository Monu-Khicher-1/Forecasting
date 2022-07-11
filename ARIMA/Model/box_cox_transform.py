from pandas import Series, read_csv
from scipy.stats import boxcox
from matplotlib import pyplot
from statsmodels.graphics.gofplots import qqplot
series = read_csv('../Src/electricity_data.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
X = series.MCP.values
transformed, lam = boxcox(X)
print('Lambda: %f' % lam)
pyplot.plot(transformed)
pyplot.show()