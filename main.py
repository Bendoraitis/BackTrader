import download_data
from strategy.buy_trades_high_level.main import buy_trades_high_level
from strategy.average_true_range.main import average_true_range
from strategy.buy_trades_high_level.main import buy_trades_high_level_long_time
from strategy.LSTM_by_day.main import LSTM_strategy_by_day
from strategy.Transformer_by_day.main import Transformer_strategy_by_day
from strategy.by_high_volume.main import by_high_volume
from strategy.by_high_volume_miltiprocessing.main import by_high_volume_multiprocessing
import time
import tensorflow as tf
import os

# Run just on CPU
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Run on GPU
os.environ['XLA_FLAGS'] = '--xla_gpu_cuda_data_dir=/usr/lib/cuda'

# Print CPU and GPu
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
print("Num CPUs Available: ", len(tf.config.list_physical_devices('CPU')))

start_time = time.time()

###############################################################################
######                         Load data                                 #######                 2022-12-31 2025-05-14
###############################################################################
data_file = download_data.get_merged_coin_data_file("BTCUSDT", '15m', '2025-05-01', '2025-05-14')
# data_file = download_data.get_merged_coin_data_file("OMUSDT", '1m', '2021-03-08', '2025-02-15')
# data_file = download_data.get_merged_coin_data_file("OMUSDT", '1m', '2025-02-01', '2025-02-16')


###############################################################################
######                        Strategy run                               ######
###############################################################################
# average_true_range(data_file, 601, 601)
# buy_trades_high_level_long_time(data_file)
# LSTM_strategy_by_day(data_file, 500, 100, 6)
# Transformer_strategy_by_day(data_file, 500, 100, 2)

# by_high_volume(data_file)
by_high_volume_multiprocessing(data_file)

print("\n--- %s seconds ---" % (time.time() - start_time))
print("--- %s minutes ---" % ((time.time() - start_time) / 60))
