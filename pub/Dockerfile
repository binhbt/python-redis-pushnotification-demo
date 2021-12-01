FROM python:3.6.7
COPY pub/requirements.txt /
RUN pip3 install -r /requirements.txt

RUN mkdir -p /build
WORKDIR /build

COPY pub /build

