from kivy.lang import Builder
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
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.label import Label
# from kivy.uix.label import Label
from kivy.uix.screenmanager import CardTransition

THRESHOLD = 0
MAX_PATH_SIZE = 22


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
    result = numpy.mean(result)
    print("result:", result)

    return result > THRESHOLD


class MainScreen(Screen):
    pass


class SubScreen(Screen):
    def __init__(self, title, img, **kwargs):
        self.img = img
        self.title = title
        super(SubScreen, self).__init__(**kwargs)


class AntivirusApp(App):
    def build(self):
        self.main = MainScreen(name='main')

        self.sm = ScreenManager()
        self.sm.switch_to(self.main)

        # self.sm.add_widget()
        # self.sm.add_widget()

        Window.bind(on_dropfile=self._on_file_drop)

        return self.sm

    def _on_file_drop(self, window, file_path):
        result = run(file_path)
        file_path = file_path.decode()

        if len(file_path) > MAX_PATH_SIZE:
            file_path = file_path[:MAX_PATH_SIZE] + "..."

        if result:
            title = f"Danger! \"{file_path}\" is malware :("
            img = "malware"
        else:
            title = f"Safe! \"{file_path}\" is not malware :)"
            img = "doc2"

        self.sub = SubScreen(title, f"assets/img/{img}.png", name='sub')
        self.sm.switch_to(self.sub)

# Builder.load_file('assets/main.kv')


AntivirusApp().run()
