import io
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dropout, Dense
from sklearn.preprocessing import MinMaxScaler


def LSTM_strategy_by_day(filename, data_x_length, data_y_length, epochs):
    df = pd.read_csv(filename)

    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')

    df.index = df['open_time']
    data = df.sort_index(ascending=True, axis=0).reset_index(drop=True)

    new_dataset = pd.DataFrame(index=range(0, len(df)), columns=['open_time', 'open_price'])

    for i in range(0, len(data)):
        new_dataset["open_time"][i] = data['open_time'][i]
        new_dataset["open_price"][i] = data["open_price"][i]

    split_value = int(len(df) - data_y_length)
    train_data = new_dataset[0:split_value]

    new_dataset.index = new_dataset.open_time
    new_dataset.drop("open_time", axis=1, inplace=True)

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(new_dataset)

    x_train_data, y_train_data = [], []
    for i in range(data_x_length, len(train_data) - data_x_length):
        x_train_data.append(scaled_data[i - data_x_length:i, 0])
        y_train_data.append(scaled_data[i:i + data_y_length, 0])

    # convert to numpy
    x_train_data, y_train_data = np.array(x_train_data), np.array(y_train_data)

    # reshape it to 3D
    x_train_data = np.reshape(x_train_data, (x_train_data.shape[0], x_train_data.shape[1], 1))
    y_train_data = np.reshape(y_train_data, (y_train_data.shape[0], y_train_data.shape[1], 1))

    lstm_model = Sequential()
    lstm_model.add(LSTM(units=500, return_sequences=True, input_shape=(x_train_data.shape[1], 1)))
    lstm_model.add(LSTM(units=100))
    lstm_model.add(Dense(data_y_length))

    lstm_model.compile(loss='mean_squared_error', optimizer='adam')
    history = lstm_model.fit(x_train_data, y_train_data, epochs=epochs, batch_size=50, verbose=1)

    plot_learning_curves(history.history["loss"])
    plt.show()

    inputs_data = new_dataset[len(new_dataset) - data_x_length:].values
    inputs_data = inputs_data.reshape(-1, 1)
    inputs_data_transformed = scaler.transform(inputs_data)

    X_test = []
    X_test.append(inputs_data_transformed[0:data_x_length])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))


    predicted_open_price = lstm_model.predict(X_test)

    predicted_open_price = scaler.inverse_transform(predicted_open_price)
    predicted_open_price = predicted_open_price.reshape(data_y_length, 1)


    # train_data = new_dataset[:split_value]
    print(len(new_dataset) - data_y_length)
    valid_data = new_dataset[len(new_dataset) - data_y_length:]

    # valid_data = valid_data.assign(Predictions=predicted_open_price)

    # print(valid_data)
    plt.plot(new_dataset['open_price'], label="new_dataset", color='blue')
    # plt.plot(train_data['open_price'], label="train_data", color='yellow')
    # plt.plot(valid_data['open_price'])
    # plt.plot(valid_data['Predictions'])
    plt.plot(valid_data.index, predicted_open_price, color='red', label="Predict price")
    plt.show()
    plt.savefig('strategy/LSTM_by_day/chart.png')

def plot_learning_curves(loss):
    plt.plot(np.arange(len(loss)) + 0.5, loss, "b.-", label="Training loss")
    plt.gca().xaxis.set_major_locator(mpl.ticker.MaxNLocator(integer=True))
    plt.axis([1, 20, 0, 0.05])
    plt.legend(fontsize=14)
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.grid(True)
    plt.savefig('strategy/LSTM_by_day/learning_curves.png')