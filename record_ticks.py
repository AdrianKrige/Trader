#!/usr/bin/env python

import time
from pybitx.api import BitX
from secrets import api_key, api_secret


client = BitX(api_key, api_secret)
file = "test_data/live.txt"


def get_ticker():
    ticker = client.get_ticker()
    return ticker

with open(file, 'a') as file:
    while True:
        t = get_ticker()
        file.write('{}-{},{}\n'.format(t['timestamp'], t['bid'].split('.')[0], t['ask'].split('.')[0]))
        time.sleep(10)
