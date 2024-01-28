from datetime import datetime
import config
import pymysql
import time
import csv
import pandas as pd


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


def load_from_db():
    con = pymysql.connect(host=config.host, user=config.user, password=config.password, database=config.database,
                          charset=config.charset)
    my_cursor = con.cursor()

    begin_time = int(datetime.timestamp(datetime(2023, 10, 1))) * 1000
    end_time = int(datetime.timestamp(datetime(2023, 12, 14))) * 1000
    sql_select = f"SELECT * FROM `BTCUSDT` WHERE `open_time` BETWEEN '{begin_time}' AND '{end_time}'"
    my_cursor.execute(sql_select)

    for item in my_cursor:
        date_returned = datetime.fromtimestamp(int(item[0]) / 1000)
        print(date_returned)
        break
    con.close()
    return my_cursor


def loads_from_file_csv():
    file = open('data/backtrader.csv', 'r')
    data = list(csv.reader(file, delimiter=','))
    print(data[0])
    file.close()


def buy_trades_high_level(filename):
    orders = []
    ord_0 = Orders()
    orders.append(ord_0)

    df = pd.read_csv(filename)
    data_frame = pd.DataFrame(df)

    price_before = 0
    trades_before = 0
    for index, row in data_frame.iterrows():
        last_order = orders[-1]

        # closing/editing trade
        if last_order.open_trade_price != 0 and last_order.close_trade_price == 0:
            last_order.set_log(row)

            # closing buy order
            if row['close_price'] < price_before and last_order.buy_or_sell == 'buy':
                last_order.close_trade_price = row['close_price']
                open_fee = last_order.open_trade_price * last_order.broker_fee
                close_fee = last_order.close_trade_price * last_order.broker_fee
                last_order.profit = (((last_order.close_trade_price - last_order.open_trade_price)
                                      * last_order.size_lot) - open_fee - close_fee)
                ord_1 = Orders()
                orders.append(ord_1)

            # closing sell order
            if row['close_price'] > price_before and last_order.buy_or_sell == 'sell':
                last_order.close_trade_price = row['close_price']
                open_fee = last_order.open_trade_price * last_order.broker_fee
                close_fee = last_order.close_trade_price * last_order.broker_fee
                last_order.profit = (((last_order.open_trade_price - last_order.close_trade_price)
                                      * last_order.size_lot) - open_fee - close_fee)

                ord_1 = Orders()
                orders.append(ord_1)

        # opening trade
        if row['trades'] > 1000 and trades_before > 1000 and last_order.open_trade_price == 0:
            last_order.open_trade_price = row['close_price']
            if price_before <= row['close_price']:
                last_order.buy_or_sell = "buy"
            else:
                last_order.buy_or_sell = 'sell'
            # print(f'Open {last_order.buy_or_sell} order on: {last_order.open_trade_price}')
            last_order.set_log(row)

        price_before = row['close_price']
        trades_before = row['trades']
    return orders


def buy_trades_high_level_long_time(filename):
    orders = []
    ord_0 = Orders()
    orders.append(ord_0)

    df = pd.read_csv(filename)
    data_frame = pd.DataFrame(df)

    price_before = 0
    trades_before = 0
    open_seconds_count = 0
    for index, row in data_frame.iterrows():
        last_order = orders[-1]

        # closing/editing trade
        if last_order.open_trade_price != 0 and last_order.close_trade_price == 0:
            last_order.set_log(row)

            # closing buy order
            if open_seconds_count == 3600 and last_order.buy_or_sell == 'buy':
                last_order.close_trade_price = row['close_price']
                open_fee = last_order.open_trade_price * last_order.broker_fee
                close_fee = last_order.close_trade_price * last_order.broker_fee
                last_order.profit = (((last_order.close_trade_price - last_order.open_trade_price)
                                      * last_order.size_lot) - open_fee - close_fee)
                ord_1 = Orders()
                orders.append(ord_1)

            # closing sell order
            if open_seconds_count == 3600 and last_order.buy_or_sell == 'sell':
                last_order.close_trade_price = row['close_price']
                open_fee = last_order.open_trade_price * last_order.broker_fee
                close_fee = last_order.close_trade_price * last_order.broker_fee
                last_order.profit = (((last_order.open_trade_price - last_order.close_trade_price)
                                      * last_order.size_lot) - open_fee - close_fee)

                ord_1 = Orders()
                orders.append(ord_1)

        # opening trade
        if row['trades'] > 1000 and trades_before > 1000 and last_order.open_trade_price == 0:
            last_order.open_trade_price = row['close_price']
            if price_before <= row['close_price']:
                last_order.buy_or_sell = "sell"
            else:
                last_order.buy_or_sell = 'buy'
            # print(f'Open {last_order.buy_or_sell} order on: {last_order.open_trade_price}')
            last_order.set_log(row)
            open_seconds_count = 0

        price_before = row['close_price']
        trades_before = row['trades']
        open_seconds_count += 1
    return orders


# start_time = time.time()
#
#
#
#
#
# print('\nExecution time:', time.time() - start_time, 'seconds')
