#!/usr/bin/env python

from mock_luno import Mock
# from trader import Trader
# from trader2 import Trader
from trader3 import Trader

zar = 10000
btc = 0.05

# 0.0406 + 0.05 = 0.0906 = R19568.7846 Without trading

transaction_amount = 0.0005
offset = 1000.00

m = Mock(zar, btc, file='test_data/charts.txt')
t = Trader('mock-key', 'mock-secret', mock=m, amount=transaction_amount, offset=offset)

t.run()
