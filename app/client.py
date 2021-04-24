import syft as sy
import tensorflow as tf
import numpy
import time

from dataset import get_dataset

hook = sy.KerasHook(tf.keras)
client = sy.TFEWorker()

alice = sy.TFEWorker(host='model_owner:4000')
bob = sy.TFEWorker(host='model_owner:4001')
carol = sy.TFEWorker(host='model_owner:4002')

cluster = sy.TFECluster(alice, bob, carol)
client.connect_to_model((1, 32, 32, 1), ((1, 25)), cluster)

_, test_X, _, test_Y = get_dataset()

time.sleep(5)

for x, y in zip(test_X, test_Y):
    x = x.reshape(32, 32, 1)

    print('send query')
    print("label:", y)

    result = client.query_model(numpy.array([x]))
    print("result:", numpy.mean(result))

    time.sleep(1)
