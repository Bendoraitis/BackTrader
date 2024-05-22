import io
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout, LayerNormalization, MultiHeadAttention, GlobalAveragePooling1D
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler

def Transformer_strategy_by_day(filename, data_x_length, data_y_length, epochs):
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

    x_train_data, y_train_data, x_test_data, y_test_data = [], [], [], []
    for i in range(data_x_length, len(train_data) - data_x_length):
        x_train_data.append(scaled_data[i - data_x_length:i, 0])
        x_test_data.append(scaled_data[i:i+data_x_length, 0])
        y_train_data.append(scaled_data[i:i + data_y_length, 0])
        y_test_data.append(scaled_data[i + data_x_length:i + data_x_length + data_y_length, 0])

    x_train_data, y_train_data, x_test_data, y_test_data = np.array(x_train_data), np.array(y_train_data), np.array(x_test_data), np.array(y_test_data)

    def transformer_encoder(inputs, head_size, num_heads, ff_dim, dropout=0):
        x = MultiHeadAttention(key_dim=head_size, num_heads=num_heads, dropout=dropout)(inputs, inputs)
        x = Dropout(dropout)(x)
        x = LayerNormalization(epsilon=1e-6)(x)
        res = x + inputs

        x = Dense(ff_dim, activation="relu")(res)
        x = Dropout(dropout)(x)
        x = Dense(inputs.shape[-1])(x)
        x = LayerNormalization(epsilon=1e-6)(x)
        return x + res

    input_shape = (x_train_data.shape[1], 1)
    inputs = Input(shape=input_shape)
    x = transformer_encoder(inputs, head_size=256, num_heads=4, ff_dim=4, dropout=0.1)
    x = GlobalAveragePooling1D()(x)
    x = Dropout(0.1)(x)
    outputs = Dense(data_y_length)(x)

    transformer_model = Model(inputs, outputs)
    transformer_model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=1e-4))
    history = transformer_model.fit(x_train_data, y_train_data, epochs=epochs, batch_size=50, verbose=1, validation_data=(x_test_data, y_test_data))

    plot_learning_curves(history.history["loss"])
    plt.show()

    inputs_data = new_dataset[len(new_dataset) - data_x_length:].values
    inputs_data = inputs_data.reshape(-1, 1)
    inputs_data_transformed = scaler.transform(inputs_data)

    X_test = []
    X_test.append(inputs_data_transformed[0:data_x_length])
    X_test = np.array(X_test)

    predicted_open_price = transformer_model.predict(X_test)

    predicted_open_price = scaler.inverse_transform(predicted_open_price)
    predicted_open_price = predicted_open_price.reshape(data_y_length, 1)

    valid_data = new_dataset[len(new_dataset) - data_y_length:]

    plt.plot(new_dataset['open_price'], label="new_dataset", color='blue')
    plt.plot(valid_data.index, predicted_open_price, color='red', label="Predict price")
    plt.show()
    plt.savefig('strategy/Transformer_by_day/chart.png')

def plot_learning_curves(loss):
    plt.plot(np.arange(len(loss)) + 0.5, loss, "b.-", label="Training loss")
    plt.gca().xaxis.set_major_locator(mpl.ticker.MaxNLocator(integer=True))
    plt.axis([1, 20, 0, 0.05])
    plt.legend(fontsize=14)
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.grid(True)
    plt.savefig('strategy/Transformer_by_day/learning_curves.png')
