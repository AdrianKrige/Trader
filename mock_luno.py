class Mock:
    def __init__(self, zar, btc, file):
        self.zar = zar
        self.btc = btc
        self.ticks = []
        self.orders = {'orders': []}
        self.order_id = 0
        with open(file, 'r') as file:
            self.ticks = file.readlines()
        self.ticks = [line.strip('\n') for line in self.ticks]
        # self.ticks = [{'bid': x.split('-')[1].split(',')[0], 'ask': x.split('-')[1].split(',')[1]} for x in self.ticks]
        self.ticks = [{'bid': min(x.split(',')[1], x.split(',')[4]), 'ask': max(x.split(',')[1], x.split(',')[4])} for x in self.ticks]


    def get_ticker(self):
        tick = self.ticks.pop(0)
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
        return tick

    def stop_order(self, order_id):
        l = len(self.orders['orders'])
        for order in self.orders['orders']:
            if order['order_id'] == order_id:
                self.orders['orders'].remove(order)
        assert len(self.orders['orders']) == (l-1)
        return True

    # {u'fee_counter': u'0.00', u'zar': u'0.00', u'order_id': u'BXCD4RH6TBNZWW8', u'creation_timestamp': 1514177929210,
    #  u'counter': u'0.00', u'limit_volume': u'0.0005', u'limit_price': u'217470.00', u'pair': u'XBTZAR',
    #  u'state': u'PENDING', u'base': u'0.00', u'btc': u'0.00', u'fee_zar': u'0.00', u'fee_base': u'0.00',
    #  u'type': u'ASK', u'completed_timestamp': 0, u'expiration_timestamp': 0, u'fee_btc': u'0.00'}
    # Order needs
    # {'type': 'ASK/BID', 'order_id': 'BXCD4RH6TBNZWW8', 'limit_volume': 0.0005, 'limit_price': 217470.00}
    # order_id = self.client.create_limit_order(order_type, volume, price)
    def create_limit_order(self, type, volume, price):
        t = 'ASK' if type == 'sell' else 'BID'
        if not self.can_create_order(t, volume, price):
            return Exception
        order = {'type': t, 'order_id': self.order_id, 'limit_volume': volume, 'limit_price': price}
        self.order_id += 1
        self.orders['orders'].append(order)
        return order['order_id']

    def get_orders(self, status='PENDING'):
        return self.orders

    # test methods
    def get_ticks(self):
        print(self.ticks)

    def can_create_order(self, type, volume, price):
        if type == 'ASK':
            if (self.btc - volume) < 0:
                return False
        else:
            if (self.zar - volume*price) < 0:
                return False
        return True
