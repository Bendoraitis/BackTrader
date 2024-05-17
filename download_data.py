import csv
import requests
import os
import shutil
import pymysql.cursors
import config
from datetime import date
import datetime


def get_coin_data_file(coin="BTCUSDT", interval='1s', coin_date="2017-08-18"):
    """
    https://binance-docs.github.io/apidocs/spot/en/#compressed-aggregate-trades-list

    getting files from e.g: https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1s/BTCUSDT-1s-2017-08-18.zip URL
    files from browser: https://data.binance.vision/?prefix=data/spot/daily/klines/BTCUSDT/1s/

    file format using(0, 1, 2, 3, 4, 6, 8), not using(5,7,9,10,11):
    [
      [
        1499040000000,      // Kline open time
        "0.01634790",       // Open price
        "0.80000000",       // High price
        "0.01575800",       // Low price
        "0.01577100",       // Close price
        "148976.11427815",  // Volume
        1499644799999,      // Kline Close time
        "2434.19055334",    // Quote asset volume
        308,                // Number of trades
        "1756.87402397",    // Taker buy base asset volume
        "28.46694368",      // Taker buy quote asset volume
        "0"                 // Unused field, ignore.
      ]
    ]
    """

    path = "data/" + coin + "-" + interval
    file_name = coin + "-" + interval + "-" + coin_date  #

    if not os.path.exists(path):
        os.mkdir(path)

    # if we don't have file, download and unzip to csv
    try:
        open(path + "/" + file_name + ".csv")
        return f"File exists in {path}/{file_name}.csv"
    except FileNotFoundError:
        url = "https://data.binance.vision/data/spot/daily/klines/" + coin + "/" + interval + "/" + file_name + ".zip"
        file = requests.get(url, stream=True)

        if file.status_code == 200:
            dump = file.raw

            with open(path + "/" + file_name + ".zip", 'wb') as location:
                shutil.copyfileobj(dump, location)
                del dump
                location.close()
            shutil.unpack_archive(path + "/" + file_name + ".zip", path)
            os.remove(path + "/" + file_name + ".zip")
            return f"File downloaded in {path}/{file_name}.csv"
        else:
            return f"No such file in cloud: {url}"


def insert_coin_data_to_db(coin="BTCUSDT", interval="1s", coin_date="2017-08-18"):
    """
    Loading coin data from file, removing unnecessary data and writing to database.
    Creating table if we have new coin.
    :param coin:
    :param interval: time interval e.g "1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h" or "1d"
    :param coin_date:
    :return:
    """
    with open(f'data/{coin}-{interval}/{coin}-{interval}-{coin_date}.csv', "r") as coin_file:
        file_content = list(csv.reader(coin_file))

    for item in file_content:
        del item[11]
        del item[10]
        del item[9]
        del item[7]
        del item[5]

    con = pymysql.connect(host=config.host, user=config.user, password=config.password, database=config.database,
                          charset=config.charset)
    my_cursor = con.cursor()

    # noinspection PyBroadException
    try:
        sql_select = f"Select * FROM {coin}"
        my_cursor.execute(sql_select)
    except Exception:
        sql_create: str = (f"CREATE TABLE `{coin}` ("
                           "`open_time` varchar(13) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Kline open time', "
                           "`open_price` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Open price', "
                           "`high_price` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'High price',"
                           "`low_price` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Low price', "
                           "`close_price` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Close price', "
                           "`close_time` varchar(13) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Kline Close time',"
                           "`number_of_traders` int NOT NULL COMMENT 'Number of trades'"
                           ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
        my_cursor.execute(sql_create)
        con.commit()
        sql_index = (f"ALTER TABLE `{coin}` "
                     "ADD PRIMARY KEY (`open_time`), "
                     "ADD UNIQUE KEY `open_time` (`open_time`)")
        my_cursor.execute(sql_index)
        con.commit()

    sql_insert = f'INSERT IGNORE INTO {coin} '
    sql_insert += f'(open_time, open_price, high_price, low_price, close_price, close_time, number_of_traders) '
    sql_insert += f'VALUES (%s, %s, %s, %s, %s, %s, %s)'
    my_cursor.executemany(sql_insert, file_content)
    con.commit()

    con.close()


def get_and_insert_coin_data_files(coin="BTCUSDT", interval="1s", beguine_date='2023-12-01', end_date='2023-12-03'):
    """
    Downloading files from Binance, saving to folder as extracted file and writing to database
    :param coin: cryptocurrency pair e.g. "BTCUSDT"
    :param interval: time interval e.g "1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h" or "1d"
    :param beguine_date:
    :param end_date:
    :return:
    """
    beguine_date_list = beguine_date.split('-')
    beguine_date = date(int(beguine_date_list[0]), int(beguine_date_list[1]), int(beguine_date_list[2]))
    end_date_list = end_date.split('-')
    end_date = date(int(end_date_list[0]), int(end_date_list[1]), int(end_date_list[2]))

    if beguine_date <= end_date:
        while True:
            get_coin_data_file(coin=coin, interval=interval, coin_date=str(end_date))
            insert_coin_data_to_db(coin=coin, coin_date=str(end_date))
            end_date -= datetime.timedelta(days=1)
            if end_date < beguine_date:
                break
    else:
        print("Not working, because beguine_date is grater than end_date.")


def get_merged_coin_data_file(coin="BTCUSDT", interval='1s', beguine_date='2023-12-01', end_date='2023-12-03'):
    """
    Downloading files from Binance, saving to folder as extracted file and writing to file in file e.g: data/BTCUSD/_BTCUSDT.csv
    :param coin: cryptocurrency pair e.g. "BTCUSDT"
    :param interval: time interval e.g "1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h" or "1d"
    :param beguine_date:
    :param end_date:
    :return: file name and location e.g: data/BTCUSDT/_BTCUSDT-2023-12-22-2023-12-23.csv
    """
    raw_beguine_date = beguine_date
    raw_end_date = end_date
    beguine_date_list = beguine_date.split('-')
    beguine_date = date(int(beguine_date_list[0]), int(beguine_date_list[1]), int(beguine_date_list[2]))
    end_date_list = end_date.split('-')
    end_date = date(int(end_date_list[0]), int(end_date_list[1]), int(end_date_list[2]))

    path = "data/" + coin + "-" + interval
    if not os.path.exists(path):
        os.mkdir(path)

    result_file_name = f'{path}/_{coin}-{interval}-{raw_beguine_date}-{raw_end_date}.csv'
    if not os.path.exists(result_file_name):
        with open(result_file_name, 'w') as result_file:
            writer = csv.writer(result_file)
            writer.writerow(["open_time", "open_price", "high_price", "low_price", "close_price", "close_time", "trades"])

            while beguine_date <= end_date:
                get_coin_data_file(coin=coin, interval=interval, coin_date=str(beguine_date))
                with open(f'{path}/{coin}-{interval}-{beguine_date}.csv', "r") as coin_file:
                    file_content = list(csv.reader(coin_file))
                    for item in file_content:
                        del item[11]
                        del item[10]
                        del item[9]
                        del item[7]
                        del item[5]

                    writer.writerows(file_content)

                beguine_date += datetime.timedelta(days=1)
                coin_file.close()
        result_file.close()
    return result_file_name

