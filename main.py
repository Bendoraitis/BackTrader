import download_data
from strategy.buy_trades_high_level.main import buy_trades_high_level
from strategy.average_true_range.main import average_true_range
from strategy.buy_trades_high_level.main import buy_trades_high_level_long_time
import time
import matplotlib.pyplot as plt
import talib

import sys
import pandas as pd
# import cudf
# from numba import jit, cuda
# import numpy as np
# from numpy import genfromtxt

start_time = time.time()


data_file = download_data.get_merged_coin_data_file("BTCUSDT", '2017-08-17', '2024-04-15')
# strategy run
# average_true_range(data_file, 601, 601)


print("\n--- %s seconds ---" % (time.time() - start_time))
print("--- %s minutes ---" % ((time.time() - start_time) / 60))


