import tensorflow as tf
import syft as sy
import os

port = os.environ['PORT']

hook = sy.KerasHook(tf.keras)
woker = sy.TFEWorker(host=f'localhost:{port}', auto_managed=True)
woker.start()
