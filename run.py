#!/usr/bin/env python

from mock_luno import Mock
from trader4 import Trader

zar = 10000
btc = 0.05

# 0.0406 + 0.05 = 0.0906 = R19568.7846 Without trading

transaction_amount = 0.0005

mock = Mock(zar, btc, file='test_data/charts.txt')
trader = Trader(exchange=mock, amount=transaction_amount)

trader.run()
