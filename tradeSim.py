import marketSimulator
import pandas as pd

import matplotlib.pyplot as plt
import QSTK.qstkutil.tsutil as tsu





def main():
    (symbols, signals, dataAll, index2) = marketSimulator.main()
    curr_ownership = {} # KEY: TICKER, VALUE: NUMBER OF SHARES SOLD
    curr_cash = 10000
    fundValue = pd.Series(index = index2)
    for timestamp in index2:
        for (symbol, rating) in signals[timestamp]:
            owned = curr_ownership.get(symbol, 0)
            if rating == 0:
                if owned == 0:
                    pass
                elif owned > 0:# if we own that stock, sell all of it
                    curr_price = dataAll[symbol].Close[timestamp]
                    curr_cash += curr_price * owned
                    curr_ownership[symbol] = 0
                elif owned < 0:# if we owe that stock to someone else
                    curr_price = dataAll[symbol].Close[timestamp]
                    curr_cash -= curr_price * owned
                    curr_ownership[symbol] = 0
            elif (rating > 0) or (rating > 0):# buy signal
                amt = rating * 100
                # print "BOUGHT ", amt ,"", symbol, "SHARES ON ", timestamp
                curr_price = dataAll[symbol].Close[timestamp]
                curr_ownership[symbol] = owned + amt 
                curr_cash -= amt * curr_price
        fundValue[timestamp] = computeStockValue(curr_ownership, dataAll, timestamp, sorted(list(index2))) +  curr_cash
    print fundValue
    plt.clf()
    plt.plot(fundValue)
    plt.savefig('fund.pdf', format='pdf')
    
    plt.clf()
    tsu.returnize1(fundValue.values)
    plt.plot(fundValue.index, fundValue.values)
    plt.xlabel("date")
    plt.ylabel("returns",)
    plt.savefig("returns.pdf", format = 'pdf')
    return fundValue
                
                
    
    
def computeStockValue(ownership, dataAll, time, timestamps):
    total = 0.0
    for symbol in ownership.keys():
        total += lastKnownPrice(symbol, dataAll,timestamps, time) * ownership[symbol]
    return total
        
    
    
def lastKnownPrice(symbol, dataAll, timestamps, time):
    curr_index = timestamps.index(time)
    time2 = time
    while curr_index >= 0:
        if time2 in dataAll[symbol].Close.index:
            if time != time2:
                print "INTIAL TIME: ", time
                print "CHOSEN TIME: ", time2
            return dataAll[symbol].Close[time2]
        else:
            curr_index = curr_index - 1
            time2 = timestamps[curr_index]
    print "INACCURACY"
    return 0
    
    
main()