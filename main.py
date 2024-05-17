import numpy as np
import keras
import matplotlib.pyplot as plt
import matplotlib as mpl
import download_data
from strategy.buy_trades_high_level.main import buy_trades_high_level
from strategy.average_true_range.main import average_true_range
from strategy.buy_trades_high_level.main import buy_trades_high_level_long_time
from strategy.LSTM.main import LSTM_strategy
from strategy.LSTM_by_day.main import LSTM_strategy_by_day
from strategy.Transformer.main import transformer
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

data_file = download_data.get_merged_coin_data_file("BTCUSDT", '1m', '2023-10-15', '2023-10-21') #, '2023-10-15', '2024-03-10'

# strategy run
# average_true_range(data_file, 601, 601)
# buy_trades_high_level_long_time(data_file)
# LSTM_strategy(data_file)
LSTM_strategy_by_day(data_file, 20, 5, 100)
# transformer(data_file)

print("\n--- %s seconds ---" % (time.time() - start_time))
print("--- %s minutes ---" % ((time.time() - start_time) / 60))


