import time

from pybitx.api import BitX


class Trader:
    def __init__(self, exchange, amount=0.0005, offset=1000.00):
        # if mock:
        #     self.client = mock
        # else:
        #     self.client = BitX(api_key, api_secret)
        self.exchange = exchange
        self.amount = amount
        self.offset = offset
        self.deltas = []
        self.alpha = 0
        self.last = None

    def get_ticker(self):
        ticker = self.client.get_ticker()
        return ticker

    def create_order(self, order_type, volume, price):
        try:
            self.client.create_limit_order(order_type, volume, price)
        except Exception as e:
            print(e)

    def get_new_alpha(self, tick):
        elements = 1500
        current = (float(tick['ask']) + float(tick['bid'])) / 2.00
        if self.last:
            diff = current - self.last
            self.deltas.append(diff)
        self.last = current
        if len(self.deltas) > elements:
            new = sum(self.deltas[-elements:])/elements
            return new
        return None

    def check_action(self, tick):
        new = self.get_new_alpha(tick)
        if new > 0 and self.alpha > 0:
            if new > self.alpha:
                self.alpha = new
                return 'sell'
        if new < 0 and self.alpha < 0:
            if new < self.alpha:
                self.alpha = new
                return 'buy'
        self.alpha = new
        return

    def run(self):
        while True:
            try:
                tick = self.get_ticker()
            except:
                break
            action = self.check_action(tick)
            # action = 3
            # 1 = SELL, 2 = BUY, 3 = Chill
            if action == 'sell':
                self.create_order('sell', self.amount, float(tick['ask']) + 1)
            if action == 'buy':
                self.create_order('buy', self.amount, float(tick['bid']) - 1)
            # Will need to add a sleep 20 seconds here if we put this live

    def output(self, tick):
        print(sum(self.deltas))
        print(self.client.get_orders())
        print('Total: {}'.format(self.client.zar + (self.client.btc * float(tick['ask']))))
