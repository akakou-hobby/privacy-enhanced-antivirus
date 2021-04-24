import tensorflow as tf
import syft as sy
import os
import time

from cluster import get_cluster

number = os.environ['NUMBER']
number = int(number)

hook = sy.KerasHook(tf.keras)


cluster = get_cluster()
woker = cluster.workers[0]

woker.start(f'server{number}', cluster)

while True:
    time.sleep(1)
