'''
(c) 2011, 2012 Georgia Tech Research Corporation
This source code is released under the New BSD license.  Please see
http://wiki.quantsoftware.org/index.php?title=QSTK_License
for license details.

Created on January, 23, 2013

@author: Sourabh Bajaj
@contact: sourabhbajaj@gatech.edu
@summary: Event Profiler Tutorial
'''


import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep
import talib as ta
from xml.dom import minidom
"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""
def get_args(func_list):
    """given a function list (e.g [RSI, ADX]), returns the required and optional arguments"""
    value = {}    
    xmldoc = minidom.parse('./ta-lib/ta_func_api.xml')
    function_nodes = xmldoc.getElementsByTagName('FinancialFunction')
    function_nodes_relevant = []
    for function_node in function_nodes:
        curr_function = function_node.getElementsByTagName('Abbreviation')[0].firstChild.nodeValue
        if curr_function in func_list:
            function_nodes_relevant.append(function_node)
    for function_node2 in function_nodes_relevant:
        curr_function = function_node2.getElementsByTagName('Abbreviation')[0].firstChild.nodeValue
        requiredArgs = function_node2.getElementsByTagName('RequiredInputArguments')[0].getElementsByTagName('RequiredInputArgument')
        for x in requiredArgs:
            if value.has_key(curr_function):
                value[curr_function].append(x.getElementsByTagName('Name')[0].firstChild.nodeValue)
            else:
                value[curr_function] = [x.getElementsByTagName('Name')[0].firstChild.nodeValue]
    return value
    

def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    df_close = d_data['close']
    ts_market = df_close['SPY']

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            # Calculating the returns for this timestamp
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            f_marketprice_today = ts_market.ix[ldt_timestamps[i]]
            f_marketprice_yest = ts_market.ix[ldt_timestamps[i - 1]]
            f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
            f_marketreturn_today = (f_marketprice_today / f_marketprice_yest) - 1

            # Event is found if the symbol is down more then 3% while the
            # market is up more then 2%
            if f_symreturn_today <= -0.03 and f_marketreturn_today >= 0.02:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events
def find_indicators(ls_symbols, d_data):
    indicators={}
    indicator_list = ['RSI', 'ADX']
    func2args =  get_args(indicator_list)
    for a in indicator_list:
        b = copy.deepcopy(d_data['close'])
        b = b* np.NaN
        indicators[a] = b
    ldt_timestamps = d_data['close'].index
    for s_sym in ls_symbols:
        print "Finding indicators for : " + s_sym
        for i in range(0, len(ldt_timestamps)):
            for a in indicator_list:
                eval_string = 'ta.' + a + '()'
                print eval_string
                eval(eval_string)
            

if __name__ == '__main__':
    year = '2013'
    quarter = '2'
    symbol_groups = ['DJIA', 'NASDAQ', 'NYSE', 'SP500']
    names = ['djia','nasdaq', 'nyse', 'sp500']
    group = symbol_groups[2]
    grouptofile = dict(zip(symbol_groups, names))
    filename = grouptofile[group] + '-' + year + '-' + quarter
    
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    ls_symbols = np.loadtxt('./lists/' + group + '/' + filename ,dtype='S10',comments='#', skiprows=1)
    
    dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    indicators = find_indicators(ls_symbols, d_data)
    df_events = find_events(ls_symbols, d_data)
    print "Creating Study"
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename='MyEventStudy.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
