from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, ReLU, Reshape, Activation
from tensorflow.keras.layers import Conv2D, MaxPooling2D


def Model():
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='linear',
              batch_input_shape=(1, 32, 32, 1), padding='same'))
    model.add(Activation('linear'))
    model.add(MaxPooling2D(pool_size=(2, 2), padding='same'))
    model.add(Conv2D(64, (3, 3), activation='linear', padding='same'))
    model.add(Conv2D(64, (3, 3), activation='linear', padding='same'))

    model.add(Flatten())
    model.add(Dense(1024, activation='linear'))
    model.add(Activation('linear'))
    model.add(Dense(25, activation='linear'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam', metrics=['accuracy'])

    return model
