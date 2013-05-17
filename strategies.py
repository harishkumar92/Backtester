def strat1(time, analysis,data):
    if (analysis['BBANDUP'][time] < data.Close[time]):
        return -1
    elif (analysis['BBANDDOWN'][time] > data.Close[time]):
        return 1
    else:
        return 0
    