from model import Model
import tensorflow as tf
import syft as sy

import time
from cluster import get_cluster

hook = sy.KerasHook(tf.keras)

model = Model()
model.load_weights('antivirus.h5')

cluster = get_cluster()
# cluster.start()

time.sleep(5)

model.share(cluster)

print('serve...')
model.serve(num_requests=None)
