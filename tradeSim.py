import argparse
import datetime as dt
import pandas as pd
import csv
import datetime as dt

import qstkutil.qsdateutil as du
import qstkutil.DataAccess as da
import pandas.io.data as web


signals = {}
symbols = []



print "Using signals.csv"
with open ('signals.csv', 'rU') as inputFile:
    reader = csv.reader(inputFile, "excel")
    for row in reader:

        if row != []:
            print row
            time = dt.datetime(int(row[0]), int(row[1]), int(row[2]), 16, 0)
            symbols.append(row[3])
            try:
                signals[time].append([row[3], row[4], row[5]])
            except:
                signals[time] = [[row[3], row[4], row[5]]]

print "Getting data"
symbols = list(set(symbols))
startday = min(signals.keys())
endday = max(signals.keys())
timestamps = (signals.keys())
timestamps= sorted(timestamps)



current_cash = 1000000
curr_ownership={}
fundValue=[]

for symbol in symbols:
    curr_ownership[symbol] = 0

print "Computing values"

for time in timestamps:
    time2 = dt.datetime(time.year, time.month, time.day)
    if signals.has_key(time):
        for signal in signals[time]:
            symbol = signal[0]
            amt = int(signal[2])
            if signal[1] == 'BUY':
                current_cash = current_cash - (dataAll[symbol].Close[time2]* amt)
                curr_ownership[symbol] = curr_ownership[symbol] + amt
                #print str(amt) + " shares of " + symbol + " were bought"

            elif signal[1] == 'SELL':
                current_cash = current_cash + (dataAll[symbol].Close[time2]* amt)
                curr_ownership[symbol] = curr_ownership[symbol] - int(signal[2])
                #print str(amt) + " shares of " + symbol + " were sold"
            else:
                amt2 = curr_ownership[symbol]
                if (amt2 != 0):#if we have that stock, we exit the position
                    current_cash = (current_cash + (dataAll[symbol].Close[time2] * amt2))
                    curr_ownership[symbol] = 0

        stockvalue = 0
        for symbol in symbols:
            stockvalue = stockvalue + (curr_ownership[symbol] * dataAll[symbol].Close[time2])
        #print "STOCK VALUE: "  + str(stockvalue)
        print curr_ownership
        #print "CURRENT CASH: " + str(current_cash)
        print "TOTAL VALUE: " + str(stockvalue + current_cash)
        print time

        fundValue.append([time, (stockvalue + current_cash)])


print "Writing values into csv file"
with open ('performance.csv', 'w') as performance:
    writer = csv.writer(performance)
    for value in fundValue:
        writer.writerow([value[0], value[1]])