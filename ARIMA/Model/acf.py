from pandas import read_csv
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from pandas.plotting import autocorrelation_plot
from matplotlib import pyplot

series=read_csv('../Src/electricity_data.csv',header=0,index_col=0,parse_dates=True,squeeze=True)

plot_acf(series.MCP,lags=200)
pyplot.show()

plot_pacf(series.MCP)
pyplot.show()

autocorrelation_plot(series.MCP,lags=60)
pyplot.show()
