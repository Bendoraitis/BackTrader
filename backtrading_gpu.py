import cudf
# from io import StringIO

class Orders:
    account_amount = 500
    size_lot = 10_000
    broker_fee = 0.00075

    def __init__(self):
        self.open_trade_price = 0
        self.close_trade_price = 0
        self.buy_or_sell = ""
        self.log = []
        self.profit = 0

    def set_open_trade_price(self, var):
        self.open_trade_price = var

    def set_close_trade_price(self, var):
        self.close_trade_price = var

    def set_buy_or_sell(self, var):
        self.buy_or_sell = var

    def set_log(self, var):
        self.log.append(var)


def strategy_buy_trades_high_level_gpu(filename):
    orders = []
    ord_0 = Orders()
    orders.append(ord_0)

    price_before = 0
    trades_before = 0

    df = cudf.read_csv(filename)
    data_frame = cudf.DataFrame(data=df)

    for index in data_frame.index:
        last_order = orders[-1]
        row = data_frame.at[index]

        # closing/editing trade
        if last_order.open_trade_price != 0 and last_order.close_trade_price == 0:
            last_order.set_log(row)

            # closing buy order
            if float(row['close_price']) < price_before and last_order.buy_or_sell == 'buy':
                last_order.close_trade_price = float(row['close_price'])
                last_order.profit = ((last_order.open_trade_price - last_order.close_trade_price)
                                     * last_order.broker_fee * last_order.size_lot)
                # print(f'Closing buy order: {last_order.close_trade_price}')
                # print(f'Profit: {last_order.profit}', '\n')
                ord_1 = Orders()
                orders.append(ord_1)

            # closing sell order
            if float(row['close_price']) > price_before and last_order.buy_or_sell == 'sell':
                last_order.close_trade_price = float(row['close_price'])
                last_order.profit = ((last_order.open_trade_price - last_order.close_trade_price)
                                     * last_order.broker_fee * last_order.size_lot)
                # print(f'Closing sell order: {last_order.close_trade_price}')
                # print(f'Profit: {last_order.profit}', '\n')
                ord_1 = Orders()
                orders.append(ord_1)

        if int(row['trades']) > 100 and trades_before > 100 and last_order.open_trade_price == 0:
            last_order.open_trade_price = float(row['close_price'])
            if price_before <= float(row['close_price']):
                last_order.buy_or_sell = "buy"
            else:
                last_order.buy_or_sell = 'sell'
            # print(f'Open {last_order.buy_or_sell} order on: {last_order.open_trade_price}')
            last_order.set_log(row)

        price_before = float(row['close_price'])
        trades_before = int(row['trades'])
    return orders



# start_time = time.time()
#
#
#
#
#
# print('\nExecution time:', time.time() - start_time, 'seconds')
