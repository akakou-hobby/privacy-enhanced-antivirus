import numpy
import subprocess
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split


def get_dataset():
    X = []
    Y = []

    labels = ['nomalware', 'malware']

    # num_classes is how many class you in your data
    for index, name in enumerate(labels):
        data_files = subprocess.getoutput(
            f'ls /app/data/{name}/out/').split('\n')

        for data_file in data_files:
            data_file = data_file.replace(' ', '')
            data_path = f'/app/data/{name}/out/{data_file}'
            data = numpy.load(data_path)

            data.resize(1024)

            X.append(data)
            Y.append(index)

    train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.1)

    train_X = numpy.array(train_X)
    train_X = train_X.reshape(-1, 32, 32, 1)

    train_Y = numpy.array(train_Y)
    train_Y = to_categorical(train_Y, 25)

    return train_X, test_X, train_X, test_Y
