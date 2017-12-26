import time

from pybitx.api import BitX


class Trader:
    def __init__(self, api_key, api_secret, amount=0.0005, offset=1000.00, mock=None, sleep=None):
        if mock:
            self.client = mock
        else:
            self.client = BitX(api_key, api_secret)
        self.amount = amount
        self.offset = offset
        self.sleep = sleep

    def get_ticker(self):
        ticker = self.client.get_ticker()
        return ticker

    def update_buy_create_sell(self, pending, tick):
        bids = []
        asks = []
        for order in pending:
            if 'ASK' in order.values():
                asks.append(order)
            else:
                bids.append(order)
        if len(asks) != 0:
            # buy order went off, do nothing and wait for sell order for now
            # return
            assert self.client.stop_order(asks[0]['order_id'])
        if len(bids) != 0:
            assert self.client.stop_order(bids[0]['order_id'])

        # We must now create new buy and sell orders
        buy_price, sell_price = float(tick['bid']) - self.offset, float(tick['ask']) + self.offset
        print('Create a buy order for {} @ {}'.format(self.amount, buy_price))
        self.create_order('buy', self.amount, buy_price)
        print('Create a sell order for {} @ {}'.format(self.amount, sell_price))
        self.create_order('sell', self.amount, sell_price)

    def create_order(self, order_type, volume, price):
        try:
            self.client.create_limit_order(order_type, volume, price)
        except:
            print("INSUFFICEINT FUNDS")

    def run(self):
        while True:
            tick = self.get_ticker()
            pending = self.client.get_orders('PENDING')['orders'] or []
            if len(pending) < 2:
                self.update_buy_create_sell(pending, tick)
            print("---SUMMARY---")
            print(pending)
            print(self.client.zar)
            print(self.client.btc)
            print('{} - {}'.format(tick['bid'], tick['ask']))
            # This isn't 100% accurate because using the ask price
            print('Total: {}'.format(self.client.zar + (self.client.btc*float(tick['ask']))))
            print
            if self.sleep:
                time.sleep(self.sleep)
