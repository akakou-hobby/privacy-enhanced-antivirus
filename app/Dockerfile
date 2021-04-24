FROM python:3.7.10-buster

RUN apt-get -y update && apt-get -y install curl git wget
RUN pip3 install tensorflow==1.15.5
RUN pip install tf_encrypted
RUN pip install syft==0.2.3
RUN pip install sklearn
RUN pip install pillow
RUN pip install cython

RUN apt-get install -y fftw3-dev \
    && git clone https://github.com/mertyyanik/pyleargist-python3 \
    && cd pyleargist-python3 \
    && python setup.py build \
    && python setup.py install

RUN pip install scikit-image
RUN pip install kivy 
RUN apt-get -y install libmtdev-dev
RUN apt-get -y install libgl1-mesa-dev
