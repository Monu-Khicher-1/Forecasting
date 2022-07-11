from pandas import read_csv
from pandas import DataFrame
from matplotlib import pyplot

series=read_csv('../Src/electricity_data.csv',header=0,index_col=0,parse_dates=True,squeeze=True)
series.plot()
pyplot.show()
print(series.head())
print("Done.")
