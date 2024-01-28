import talib.abstract as ta
import pandas as pd
import numpy as np
from strategy.to_files import save
import os


class Orders:
    account_amount = 500
    size_lot = 0.25
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


def average_true_range(file_name, atr_period, sma_period):
    df = pd.read_csv(file_name)
    data_frame = pd.DataFrame(df)
    atr = ta.ATR(data_frame['high_price'], data_frame['low_price'], data_frame['close_price'], timeperiod=atr_period)
    sma = ta.SMA(data_frame['close_price'], period=sma_period)

    data_frame['atr'] = atr
    data_frame['sma'] = sma

    orders = []
    ord_0 = Orders()
    orders.append(ord_0)

    for index, row in data_frame.iterrows():
        last_order = orders[-1]

        # closing/editing trade
        if last_order.open_trade_price != 0 and last_order.close_trade_price == 0:
            row['close_price_minus_sma'] = str(int(row['close_price'] - row['sma']))
            last_order.set_log(row)

            # closing buy order
            if row['atr'] < 1 and row['sma'] > row['close_price'] and last_order.buy_or_sell == 'buy':
                last_order.close_trade_price = row['close_price']
                open_fee = last_order.open_trade_price * last_order.broker_fee
                close_fee = last_order.close_trade_price * last_order.broker_fee
                last_order.profit = (((last_order.close_trade_price - last_order.open_trade_price)
                                      * last_order.size_lot) - open_fee - close_fee)
                ord_1 = Orders()
                orders.append(ord_1)

        # opening trade (buy)
        if row['atr'] > 1 and row['sma'] < row['close_price'] and (row['close_price'] - row['sma']) > 13 and last_order.open_trade_price == 0:
            last_order.open_trade_price = row['close_price']
            last_order.buy_or_sell = 'buy'
            row['close_price_minus_sma'] = str(int(row['close_price'] - row['sma']))
            last_order.set_log(row)

    naming = f'first_def_atr_{atr_period}_sma_{sma_period}'
    save(orders, os.path.dirname(os.path.abspath(__file__)), naming)

    return orders
