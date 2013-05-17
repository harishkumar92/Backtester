import pandas.io.data as web
import pandas as pd
import talib as ta
import datetime
import pprint
from collections import defaultdict
import strategies
import numpy as np

def generateSignals(symbol, dataAll, orders):
    data = dataAll[symbol]

    analysis = pd.DataFrame(index = data.index)
    timestamps = analysis.index

    analysis['ADX'] = ta.ADX(data.High, data.Low, data.Close)
    analysis['RSI'] = ta.RSI(data.Close)
    analysis['SMA5'], analysis['SMA10'], analysis['SMA20'] = ta.SMA(data.Close,5), ta.MA(data.Close,10), ta.MA(data.Close,20)
    analysis['PLUS_DI'] = ta.PLUS_DM(data.High, data.Low)
    analysis['MINUS_DI'] = ta.MINUS_DM(data.High, data.Low)
    analysis['BBANDUP'], analysis['BBANDDOWN'] = (ta.BBANDS(data.Close,20,2,1.5))[0], (ta.BBANDS(data.Close,20,2,1.5))[1]
    analysis['%K'], analysis['%D'] = ta.STOCHF(data.High, data.Low, data.Close)

    for time in timestamps:
        orders.append([time, symbol, strategies.strat1(time, analysis, data)])





def main():
    
    print "Getting Symbols"
    # symbols = np.loadtxt('sp5002012.txt',dtype='S10',comments='#', skiprows=1)
    symbols = ['DEO', 'CVX', 'KIM', 'SPY', 'DELL', 'CAT' ]
    startday = datetime.date(2012, 1 , 1)
    endday = datetime.date(2012, 12, 31)
    
    #Get index
    index = web.get_data_yahoo("SPY", startday, endday).index
    
    print "Getting Data"
    dataAll = {}
    for symbol in symbols:
        try:
            dataAll[symbol] = web.get_data_yahoo(symbol, startday, endday)
            if len(dataAll[symbol].index) != 250:
                print symbol, len(dataAll[symbol].index)
        except:
            print "Could not obtain data for: " + symbol
        
    print "Analyzing Signals"
    print dataAll['DEO']
    signals = []
    for symbol in dataAll.keys():
        generateSignals(symbol,dataAll, signals)
    signals2 = defaultdict(list)
    for timestamp, symbol, rating in signals:
        signals2[timestamp].extend([[symbol, rating]])
    return (dataAll.keys(), signals2, dataAll, index)
    
main()
