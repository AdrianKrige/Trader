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
        self.deltas = []
        self.alpha = 0
        self.last = None

    def get_ticker(self):
        ticker = self.client.get_ticker()
        return ticker

    def create_order(self, order_type, volume, price):
        try:
            self.client.create_limit_order(order_type, volume, price)
        except:
            print("INSUFFICEINT FUNDS")

    def get_new_alpha(self, tick):
        elements = 1500
        current = (float(tick['ask']) + float(tick['bid'])) / 2.00
        with open('price.csv', 'a') as file:
            file.write('{}\n'.format(current))
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
                with open('alphas600.csv', 'a') as file:
                    file.write('{}\n'.format(new))
                return 'sell'
        if new < 0 and self.alpha < 0:
            if new < self.alpha:
                self.alpha = new
                with open('alphas600.csv', 'a') as file:
                    file.write('{}\n'.format(new))
                return 'buy'
        self.alpha = new
        with open('alphas600.csv', 'a') as file:
            file.write('{}\n'.format(new))
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
            if self.sleep:
                time.sleep(self.sleep)
        self.p(tick)

    def p(self, tick):
        # pass
        # print("---SUMMARY---")
        # print(self.client.zar)
        # print(self.client.btc)
        # print('{} - {}'.format(tick['bid'], tick['ask']))
        # # This isn't 100% accurate because using the ask price
        print(sum(self.deltas))
        print(self.client.get_orders())
        print('Total: {}'.format(self.client.zar + (self.client.btc * float(tick['ask']))))
        # print