import array
import scipy
import os
import syft as sy
import tensorflow as tf
import numpy
import time
import scipy
import sys

from dataset import get_dataset
from cluster import get_cluster

from PIL import Image
import leargist
from skimage import transform
from imageio import imsave

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.label import Label


def read_file(filepath):
    with open(filepath, 'rb') as f:
        ln = os.path.getsize(filepath)
        width = 256
        rem = ln % width
        a = array.array("B")
        a.fromfile(f, ln-rem)

    g = numpy.reshape(a, (int(len(a) / width), width))
    g = numpy.uint8(g)

    print(g)

    imsave('/tmp/tmp.png', g)
    pilimg = Image.open('/tmp/tmp.png')
    img_resized = pilimg.resize((64, 64))

    desc = leargist.color_gist(img_resized)
    data = desc[0:1024]

    data = numpy.resize(data, 1024)
    data = data.reshape(32, 32, 1)

    return data


def run(filepath):
    hook = sy.KerasHook(tf.keras)
    client = sy.TFEWorker()

    cluster = get_cluster()
    client.connect_to_model((1, 32, 32, 1), ((1, 25)), cluster)

    _, test_X, _, test_Y = get_dataset()

    # time.sleep(5)

    data = read_file(filepath)

    result = client.query_model(numpy.array([data]))
    print("result:", numpy.mean(result))


class AntivirusApp(App):
    def build(self):
        Window.bind(on_dropfile=self._on_file_drop)
        return Label(text='DRAG AND DROP HERE!', font_size='20sp')

    def _on_file_drop(self, window, file_path):
        print(file_path)
        run(file_path)


AntivirusApp().run()
