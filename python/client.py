import logging
import sys

import grpc

import adafruit_pb2
import adafruit_pb2_grpc
import common
from google.protobuf import empty_pb2


def run(server):
    logging.info("connecting to server {}".format(server))
    with grpc.insecure_channel('{}:{}'.format(server, common.PORT)) as channel:
        stub = adafruit_pb2_grpc.AHT20Stub(channel)
        response = stub.Measure(request=empty_pb2.Empty())
    print('Temperature: {:.2f}°C'.format(response.temperature))
    print('Relative Humidity: {:.2f}%'.format(response.relative_humidity))


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    run(sys.argv[1])
