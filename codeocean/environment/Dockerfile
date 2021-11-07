# hash:sha256:81fc51e73ddd6029e9526f5457f88ec9b416bf7420333c43c85edf033cece962
FROM registry.codeocean.com/codeocean/tensorflow:1.4.0-python2.7.12-cuda8.0.61-cudnn6.0.21-ubuntu16.04

ARG DEBIAN_FRONTEND=noninteractive

RUN pip install -U --no-cache-dir --upgrade-strategy=only-if-needed \
    numpy==1.16.6 \
    pandas==0.24.2
