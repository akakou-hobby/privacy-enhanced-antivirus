from model import Model
import tensorflow as tf
import syft as sy

hook = sy.KerasHook(tf.keras)

model = Model()
model.load_weights('antivirus.h5')

alice = sy.TFEWorker(host='model_owner:4000', auto_managed=True)
bob = sy.TFEWorker(host='model_owner:4001', auto_managed=True)
carol = sy.TFEWorker(host='model_owner:4002', auto_managed=True)

cluster = sy.TFECluster(alice, bob, carol)
cluster.start()

model.share(cluster)

print('serve...')
model.serve(num_requests=None)
