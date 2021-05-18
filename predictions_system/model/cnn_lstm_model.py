from tensorflow import keras

from predictions_system.model.model import Model


class CNNLSTMModel(Model):
    def build_model(self, *args, **kwargs):
        model = keras.Sequential()
        print(self.input_shape)
        model.add(
            keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=self.input_shape))
        model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Dropout(0.1))

        model.add(
            keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
        model.add(keras.layers.MaxPooling2D(pool_size=(3, 3)))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Dropout(0.1))

        model.add(
            keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
        model.add(keras.layers.MaxPooling2D(pool_size=(4, 4)))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Dropout(0.1))

        model.add(
            keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same'))
        model.add(keras.layers.MaxPooling2D(pool_size=(4, 4)))
        model.add(keras.layers.BatchNormalization())
        model.add(keras.layers.Dropout(0.1))

        print(model.output_shape)
        model.add(keras.layers.Reshape((6, 64)))
        print(model.output_shape)
        # define LSTM layers
        model.add(keras.layers.LSTM(64, return_sequences=True))
        model.add(keras.layers.Dropout(0.3))
        model.add(keras.layers.LSTM(64, return_sequences=False))
        model.add(keras.layers.Dropout(0.3))

        model.add(keras.layers.Dense(self.output_size, activation='softmax'))

        optimiser = keras.optimizers.Adam(learning_rate=0.0001)

        model.compile(optimizer=optimiser,
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        model.build()
        model.summary()
        return model
