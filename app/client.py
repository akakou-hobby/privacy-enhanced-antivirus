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
from kivy.uix.button import Button


class TestApp(App):
    def build(self):
        return Button(text='Hello World')


TestApp().run()


def read_file():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'test.exe'

    with open(filename, 'rb') as f:
        ln = os.path.getsize(filename)
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


def run():
    hook = sy.KerasHook(tf.keras)
    client = sy.TFEWorker()

    cluster = get_cluster()
    client.connect_to_model((1, 32, 32, 1), ((1, 25)), cluster)

    _, test_X, _, test_Y = get_dataset()

    # time.sleep(5)

    data = read_file()

    result = client.query_model(numpy.array([data]))
    print("result:", numpy.mean(result))


eel.init("assets")
eel.start("main.html", mode="firefox")
