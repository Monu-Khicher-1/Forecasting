from cProfile import label
from cgi import test
from pandas import read_csv
from pandas import DataFrame
from matplotlib import pyplot 
from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from pandas import Series
import numpy


############################################################################################################
#----------------------------------------Some Helping Functions---------------------------------------------
############################################################################################################

def test_stationarity(timeseries):
    #Determing rolling statistics
    rolmean = timeseries.rolling(12).mean()
    rolstd = timeseries.rolling(12).std()
    #Plot rolling statistics:
    pyplot.plot(timeseries, color='blue',label='Original')
    pyplot.plot(rolmean, color='red', label='Rolling Mean')
    pyplot.plot(rolstd, color='black', label = 'Rolling Std')
    pyplot.legend(loc='best')
    pyplot.title('Rolling Mean and Standard Deviation')
    pyplot.show(block=False)

    #perform dickey fuller test  
    print("Results of dickey fuller test")
    adft = adfuller(timeseries)
    # output for dft will give us without defining what the values are.
    #hence we manually write what values does it explains using a for loop
    output = pd.Series(adft[0:4],index=['Test Statistics','p-value','No. of lags used','Number of observations used'])
    for key,values in adft[4].items():
        output['critical value (%s)'%key] =  values
    print(output)




###########################################################################################################
###########################################################################################################
#---------------------------------------Data Preparation--------------------------------------------------
###########################################################################################################
###########################################################################################################


# Loading the data

series=read_csv('./Src/Electric_Production.csv',header=0,index_col=0,parse_dates=True,squeeze=True)

# Ploting different graphs for data

series.plot()
pyplot.title("Electricity Consumption")
pyplot.xlabel("Date")
pyplot.ylabel("Consumption")
pyplot.show()

series.plot(style='k.')
pyplot.title("Electricity Consumption")
pyplot.xlabel("Date")
pyplot.ylabel("Consumption")
pyplot.show()
print(series.head())
print("Done.")

# Separating out trend and seasonal components.

result=seasonal_decompose(series,model='additive',period=12)
result.plot()
pyplot.title("Additive")
pyplot.show()

result=seasonal_decompose(series,model='multiplicative',period=12)
result.plot()
print(result)
pyplot.title("Multiplicative")
pyplot.show()

seasonality=Series(result.seasonal)
seasonality.index=series.index[:len(seasonality)]
print(seasonality.head(24))

residuals=Series(result.resid)
print(residuals.head(18))

trend=Series(result.trend)
print(trend)

# test_stationarity(trend)

# Rolling mean

rolmean=series.rolling(12).mean()

print(rolmean.head(360))

rolmean.to_csv('./Src/rolmean.csv',header=False)

pyplot.plot(series,color='blue',label='Orignal')
pyplot.plot(rolmean,color='red', label='Rolling Mean(12)')
# pyplot.plot([None for x in range(12)]+[rolmean[x]*rolmean[x] for x in range(12,len(rolmean))], color='green')

pyplot.title('Rolling Mean of Data')
pyplot.show()


#======================
# Seasonal(A)
#======================

seasonal_comp=read_csv('./Src/seasonal(A).csv',header=None,index_col=None)

count=0
seasonality=[0,0,0,0,0,0,0,0,0,0,0,0]
for i in range(0,len(seasonal_comp)-1,12):
    if(seasonal_comp.values[i]!=None):
        for j in range(12):
            seasonality[j]+=float(seasonal_comp.values[i+j])
        count+=1
print("===========================================")
print("<--------------------------------------->")
print("Seasonality: ", end=" ")
print(seasonality)
print("Count: ",count)


for i in range(12):
    seasonality[i]=float(seasonality[i])/float(count)

print(seasonality)

numpy.save('seasonality.npy',seasonality)

pyplot.plot(seasonality)
pyplot.show()


residuals=list()
for_adf_residuals=list()
for i in range(len(rolmean)):
    if(rolmean[i]==None):
        residuals.append(None)
    else: 
        residuals.append(float(series.values[i])-(float(rolmean[i])+seasonality[i%12]))
        for_adf_residuals.append(float(series.values[i])-(float(rolmean[i])+seasonality[i%12]))

Trend=read_csv('./Src/rolmean.csv',header=None,index_col=None)

Residual=Series(residuals)
Residual.to_csv('./Src/residuals.csv',header=False)

pyplot.plot(residuals)
pyplot.show()

Residual=read_csv('./Src/residual_error(A).csv',header=None,index_col=None)


print("Results of dickey fuller test")
result=adfuller(Residual)

# Result of add fuller test
print("--------------------------------------------------------------")
print("- For Residual Errors")
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))


#=======================================
#----------Log transformed data------
#=======================================

##########################################################################
##########################################################################


