# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 19:32:58 2013

Usage: python get_sp500.py >> sp500.txt
@author: harish
"""
import os
os.system("rm temp.txt")
os.system("lynx -dump http://www.stockmarketsreview.com/companies_dowjones30/ > temp.txt")

fid = open('temp.txt','r')
doAppend = 0
tickers = []
for line in fid:
    k = line.split(" ")
    if doAppend == 1: tickers.append(k[-1].strip())
    if k[-1] == 'MMM\n': doAppend = 1
    if k[-1] == 'Newsletter\n': doAppend = 0
    #print doAppend, k[-1]
for ticker in tickers[:-2]:
    print ticker
