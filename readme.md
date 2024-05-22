# Crypto Backtrader
```
   _____                      _           ____                _     _                    _             
  / ____|                    | |         |  _ \              | |   | |                  | |            
 | |      _ __  _   _  _ __  | |_  ___   | |_) |  __ _   ___ | | __| |_  _ __  __ _   __| |  ___  _ __ 
 | |     | '__|| | | || '_ \ | __|/ _ \  |  _ <  / _` | / __|| |/ /| __|| '__|/ _` | / _` | / _ \| '__|
 | |____ | |   | |_| || |_) || |_| (_) | | |_) || (_| || (__ |   < | |_ | |  | (_| || (_| ||  __/| |   
  \_____||_|    \__, || .__/  \__|\___/  |____/  \__,_| \___||_|\_\ \__||_|   \__,_| \__,_| \___||_|   
                 __/ || |                                                                              
                |___/ |_|                                                                              
```

## How to Launch
- git clone https://github.com/Bendoraitis/BackTrader
- run main.py

## Run lib install in CLI
```commandline
pip install pandas==2.2.2
pip install numpy==1.26.3
pip install keras~=2.15.0
pip install matplotlib~=3.8.4
pip install PyMySQL~=1.1.0
pip install requests~=2.31.0
pip install tensorflow==2.15.1
```

## Ta-Lib pain in the ass
<b>DO NOT USE pip install Ta-Lib !!!<b>

### For Ta-Lib best manual here:
https://medium.com/@outwalllife001/how-to-install-ta-lib-on-ubuntu-22-04-step-by-step-88ffd2507bbd 

## How get datasets
- use function:
```python
data_file = download_data.get_merged_coin_data_file("BTCUSDT", '1m', '2023-10-01', '2023-10-21')
"""
    Downloading files from Binance, saving to folder as extracted file and writing to file in file e.g: data/BTCUSD/_BTCUSDT.csv
    :param coin: cryptocurrency pair e.g. "BTCUSDT"
    :param interval: time interval e.g "1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h" or "1d"
    :param beguine_date:
    :param end_date:
    :return: file name and location e.g: data/BTCUSDT/_BTCUSDT-2023-12-22-2023-12-23.csv
"""
```
- all data will be downloaded to /data directory and merged by interval to one file. If file exists before, just loading old data
- in download_data there is few functions to use MySQL DB, but not finished, also Main project functions using files, not DB.
- but good news that MySQL also importing automatically by bulk imports, if you want to use it, change config.py credentials 

## Comment uncomment these functions to run project:
```python
# this is standard trading strategy by average true range 
average_true_range(file_name, atr_period, sma_period)
```
```python
# this is standard trading strategy by trades high level
buy_trades_high_level_long_time(filename)
```
```python
# this is LSTM model without trading strategy (will be added in future)
LSTM_strategy_by_day(filename, data_x_length, data_y_length, epochs)
```
```python
# this is Transformer model without trading strategy (will be added in future)
Transformer_strategy_by_day(filename, data_x_length, data_y_length, epochs)
```

## If you have problems on GPU
- check global variables, main.py line here:
```python
os.environ['XLA_FLAGS'] = '--xla_gpu_cuda_data_dir=/usr/lib/cuda'
```
- Also try to change not latest Tensorflow lib version
- also take care CUDA toolkit and GPU drivers. Manuals here:
- https://www.tensorflow.org/install/pip
- https://developer.nvidia.com/cuda-toolkit-archive
- https://developer.nvidia.com/cudnn

## For turning off GPU uncomment this line in main.py: 
```python
# Run just on CPU
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
```