



def generateSignalsforSymbol(symbol, dataAll, orders):
    data = dataAll[symbol]
    analysis = data.index
    timestamps = data.index

    analysis['ADX'] = ta.ADX(data.High, data.Low, data.Close)
    analysis['RSI'] = ta.RSI(data.Close)
    analysis['SMA5'], analysis['SMA10'], analysis['SMA20'] = ta.SMA(data.Close,5), ta.MA(data.Close,10), ta.MA(data.Close,20)
    analysis['PLUS_DI'] = ta.PLUS_DM(data.High, data.Low)
    analysis['MINUS_DI'] = ta.MINUS_DM(data.High, data.Low)
    analysis['BBANDUP'], analysis['BBANDDOWN'] = (ta.BBANDS(data.Close,20,2,1.5))[0], (ta.BBANDS(data.Close,20,2,1.5))[1]
    analysis['%K'], analysis['%D'] = ta.STOCHF(data.High, data.Low, data.Close)

    for i in range(0, len(timestamps)):
        if isBuy(analysis,data , i):
            orders.append([timestamps[i],symbol, 'BUY'])
        elif isSell(analysis,data, i):
            orders.append([timestamps[i],symbol, 'SELL'])
        else:
            orders.append([timestamps[i], symbol , 'OUT'])


orders = sorted(orders)
with open('signals.csv', 'w') as outFile:
    writer = csv.writer(outFile)
    for order in orders:
        writer.writerow([order[0].year , order[0].month , order[0].day, order[1], order[2], 100])
