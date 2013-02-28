import pandas.io.data as web
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
import numpy as np
from pandas import Series, DataFrame
import urllib2
import urllib
import datetime
import csv

import qstkutil.qsdateutil as du
import qstkutil.DataAccess as da


def generateSignals(symbol, dataAll, orders):
    data = dataAll[symbol]

    analysis =pd.DataFrame(index = data.index)
    timestamps = analysis.index

    analysis['ADX'] = ta.ADX(data.High, data.Low, data.Close)
    analysis['RSI'] = ta.RSI(data.Close)
    analysis['SMA5'], analysis['SMA10'], analysis['SMA20'] = ta.SMA(data.Close,5), ta.MA(data.Close,10), ta.MA(data.Close,20)
    analysis['PLUS_DI'] = ta.PLUS_DM(data.High, data.Low)
    analysis['MINUS_DI'] = ta.MINUS_DM(data.High, data.Low)
    analysis['BBANDUP'], analysis['BBANDDOWN'] = (ta.BBANDS(data.Close,20,2,1.5))[0], (ta.BBANDS(data.Close,20,2,1.5))[1]
    analysis['%K'], analysis['%D'] = ta.STOCHF(data.High, data.Low, data.Close)

    for time in timestamps:
        orders.append([time, symbol, analyseDay(time, analysis, data)])

def analyseDay(time, analysis,data):
    if (analysis['BBANDUP'][time] < data.Close[time]):
        return 'SELL'
    elif (analysis['BBANDDOWN'][time] > data.Close[time]):
        return 'BUY'
    else:
        return 'OUT'



print "Getting Symbols"
symbols = np.loadtxt('sp5002012.txt',dtype='S10',comments='#', skiprows=1)
symbols = ['GOOG', 'XOM', 'SPY', 'MSFT']
startday = datetime.date(2012, 1 , 1)
endday = datetime.date(2012, 12, 31)
timeofday = du.timedelta(hours = 16)

print "Getting Data"
dataAll = {}
for symbol in symbols:
    print "Getting data for: " + symbol
    dataAll[symbol] = web.get_data_yahoo(symbol, startday, endday)


print "Analyzing Signals"
orders = []
for symbol in symbols:
    print "Analyzing signals for: " + symbol
    generateSignals(symbol,dataAll, orders)
