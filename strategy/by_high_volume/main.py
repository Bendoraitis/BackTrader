import talib.abstract as ta
import pandas as pd
import numpy as np
from strategy import to_files
import os


class Orders:
    account_amount = 500
    size_lot = 0.25 # 0.25
    broker_fee = 0.00075 * size_lot

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

# RSI 79.9 and 5 next more than 75 - buy (ta.RSI)
# sell - SMA 25 > price
def by_high_volume(file_name):
    df = pd.read_csv(file_name)
    data_frame = pd.DataFrame(df)
    rsi = ta.RSI(data_frame['close_price'], timeperiod=20)
    sma = ta.SMA(data_frame['close_price'], period=25)

    data_frame['rsi'] = rsi
    data_frame['sma'] = sma

    orders = []
    ord_0 = Orders()
    orders.append(ord_0)

    for index, row in data_frame.iterrows():
        last_order = orders[-1]

        if index > 0:
            stop_loss = data_frame.iloc[index - 1]['low_price'] * 0.995
        else:
            stop_loss = 0  # No previous value for the first row

        # closing/editing trade
        if last_order.open_trade_price != 0 and last_order.close_trade_price == 0:
            # last_order.set_log(row)

            # closing buy order
            if stop_loss > row['close_price'] and last_order.buy_or_sell == 'buy':
                last_order.close_trade_price = row['close_price']
                open_fee = last_order.open_trade_price * last_order.broker_fee
                close_fee = last_order.close_trade_price * last_order.broker_fee
                last_order.profit = (((last_order.close_trade_price - last_order.open_trade_price)
                                      * last_order.size_lot) - open_fee - close_fee)
                ord_1 = Orders()
                orders.append(ord_1)
                last_order.set_log(row)

        # opening trade (buy)
        if row['rsi'] > 70 and last_order.open_trade_price == 0:
            last_order.open_trade_price = row['close_price']
            last_order.buy_or_sell = 'buy'
            last_order.set_log(row)

    coin_naming = to_files.get_naming_with_coin_and_date(file_name)
    naming = f'high_volume_result{coin_naming}'
    to_files.save(orders, os.path.dirname(os.path.abspath(__file__)), naming)

    return orders
