#!/usr/bin/env python

from trader import Trader
from secrets import api_key, api_secret

t = Trader(api_key, api_secret, amount=0.0005, offset=1000.00, sleep=20)
t.run()