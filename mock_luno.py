class Mock:
    """
    Mock exchange to simulate luno. Currently does not take into account fees and only implements limited api calls.
    """
    def __init__(self, zar, btc, file):
        self.zar = zar
        self.btc = btc
        self.orders = {'orders': []}
        self.order_id = 0
        with open(file, 'r') as f:
            self.ticks = f.readlines()
        self.ticks = [line.strip('\n') for line in self.ticks]
        self.ticks = [
            {
                'bid': min(x.split(',')[1], x.split(',')[4]),
                'ask': max(x.split(',')[1], x.split(',')[4])
            } for x in self.ticks]

    def get_ticker(self):
        tick = self.ticks.pop(0)
        self._trigger_orders(tick)
        return tick

    def stop_order(self, order_id):
        for order in self.orders['orders']:
            if order['order_id'] == order_id:
                self.orders['orders'].remove(order)
                return True
        return False

    def create_limit_order(self, type, volume, price):
        t = 'ASK' if type == 'sell' else 'BID'
        # Check if we have the funds to create this order
        if not self._can_create_order(t, volume, price):
            return
        order = {'type': t, 'order_id': self.order_id, 'limit_volume': volume, 'limit_price': price}
        self.order_id += 1
        self.orders['orders'].append(order)
        return order['order_id']

    def get_orders(self, status='PENDING'):
        return self.orders

    # NON luno api methods
    def _can_create_order(self, type, volume, price):
        if type == 'ASK':
            if (self.btc - volume) < 0:
                return False
        else:
            if (self.zar - volume*price) < 0:
                return False
        return True

    def _trigger_orders(self, tick):
        for order in self.orders['orders']:
            if order['type'] == 'BID':
                if order['limit_price'] > int(tick['bid']):
                    # print("BUY ORDER GOES THROUGH")
                    self.btc += order['limit_volume']
                    self.zar -= order['limit_price']*order['limit_volume']
                    self.stop_order(order['order_id'])
            else:
                if order['limit_price'] < int(tick['ask']):
                    # print("SELL ORDER GOES THROUGH")
                    self.btc -= order['limit_volume']
                    self.zar += order['limit_price']*order['limit_volume']
                    self.stop_order(order['order_id'])
