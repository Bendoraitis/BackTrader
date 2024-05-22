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

### Run lib install in CLI
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

### Comment uncomment these functions:
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

### If you have problems on GPU
- check global variables, main.py line here:
```python
os.environ['XLA_FLAGS'] = '--xla_gpu_cuda_data_dir=/usr/lib/cuda'
```
- Also try to change not latest Tensorflow lib version
- also take care CUDA toolkit and GPU drivers. Manuals here:
- https://www.tensorflow.org/install/pip
- https://developer.nvidia.com/cuda-toolkit-archive
- https://developer.nvidia.com/cudnn

### For turning off GPU uncomment this line in main.py: 
```python
# Run just on CPU
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
```