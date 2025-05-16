import talib.abstract as ta
import pandas as pd
import numpy as np
from strategy import to_files
import os
import multiprocessing
import re


class Orders:
    account_amount = 500
    size_lot = 0.025
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


def process_chunk(data_chunk):
    data_frame = pd.DataFrame(data_chunk).reset_index(drop=True)  # 👈 Reset index

    rsi = ta.RSI(data_frame['close_price'], timeperiod=20)
    sma = ta.SMA(data_frame['close_price'], timeperiod=25)
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
            stop_loss = 0

        if last_order.open_trade_price != 0 and last_order.close_trade_price == 0:
            if stop_loss > row['close_price'] and last_order.buy_or_sell == 'buy':
                last_order.close_trade_price = row['close_price']
                open_fee = last_order.open_trade_price * last_order.broker_fee
                close_fee = last_order.close_trade_price * last_order.broker_fee
                last_order.profit = (((last_order.close_trade_price - last_order.open_trade_price)
                                      * last_order.size_lot) - open_fee - close_fee)
                ord_1 = Orders()
                orders.append(ord_1)
                last_order.set_log(row)

        if row['rsi'] > 70 and last_order.open_trade_price == 0:
            last_order.open_trade_price = row['close_price']
            last_order.buy_or_sell = 'buy'
            last_order.set_log(row)

    return orders


def by_high_volume_multiprocessing(file_name):
    df = pd.read_csv(file_name)
    cpu_count = 12  # Adjust as needed
    chunks = np.array_split(df, cpu_count)

    with multiprocessing.Pool(cpu_count) as pool:
        all_orders_lists = pool.map(process_chunk, chunks)

    # Flatten the list of lists
    all_orders = [order for sublist in all_orders_lists for order in sublist]

    coin_naming = to_files.get_naming_with_coin_and_date(file_name)
    naming = f'high_volume_result{coin_naming}'

    to_files.save(all_orders, os.path.dirname(os.path.abspath(__file__)), naming)

    return all_orders


if __name__ == "__main__":
    # Example usage (ensure the main guard is used for multiprocessing)
    file_path = "your_data_file.csv"
    by_high_volume_multiprocessing(file_path)
