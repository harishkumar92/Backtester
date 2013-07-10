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
    pass
def find_indicators(ls_symbols, d_data):
    success = True
    indicators={}
    indicator_list = ['RSI']
    func2args =  get_args(indicator_list)
    for a in indicator_list:
        b = copy.deepcopy(d_data['close'])
        b = b* np.NaN
        indicators[a] = b
    failed = 0
    for s_sym in ls_symbols:
        
        print "Finding indicators for : " + s_sym
        """
        for a in indicator_list:
            
            proper_args = f(func2args, a)
            
            eval_string = 'ta.' + a + '('
            for i in range(len(proper_args) - 1):
                eval_string +=  'd_data["%s"][s_sym]' % (proper_args[i]) + ','
            eval_string += 'd_data["%s"][s_sym])' % (proper_args[len(proper_args) - 1])
            print eval_string
            try:
                indicators[a][s_sym] = eval(eval_string)
            except Exception as e:
                print e.message
                success = False
    if success:
        print "YAYAYJGSJHGDJDGJSHDSJDSDFHGSFHSFDHGSDGHSD"
    return indicators
    """
        try:
            indicators['RSI'][s_sym] = ta.RSI(d_data['close'][s_sym])
            # print indicators['RSI'][s_sym]
            print d_data['actual_close'][s_sym]
        except Exception as e:
            failed = failed + 1
            print e.message
    print float(failed) / float(len(ls_symbols))        

            
def f(func2args, func_name):
    raw_list = func2args[func_name]
    for i in range(len(raw_list)):
        if raw_list[i] == 'inReal':
            raw_list[i] = 'close'
        else:
            raw_list[i] = raw_list[i].lower()
        
    return raw_list
            
            
if __name__ == '__main__':
    year = '2013'
    quarter = '2'
    symbol_groups = ['DJIA', 'NASDAQ', 'NYSE', 'SP500']
    names = ['djia','nasdaq', 'nyse', 'sp500']
    group = symbol_groups[0]
    grouptofile = dict(zip(symbol_groups, names))
    filename = grouptofile[group] + '-' + year + '-' + quarter
    
    dt_start = dt.datetime(2012, 1, 1)
    dt_end = dt.datetime(2013, 1, 1)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))
    ls_symbols = np.loadtxt('./lists/' + group + '/' + filename ,dtype='S10',comments='#', skiprows=1)
    dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    
    
    d_data = dict(zip(ls_keys, ldf_data))
    indicators = find_indicators(ls_symbols, d_data)
    df_events = find_events(ls_symbols, d_data)
    print "Creating Study"
    #ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
    #            s_filename='MyEventStudy.pdf', b_market_neutral=True, b_errorbars=True,
    #           s_market_sym='SPY')
