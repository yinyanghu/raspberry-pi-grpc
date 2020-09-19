import logging

import grpc

import adafruit_pb2
import adafruit_pb2_grpc
import common
from google.protobuf import empty_pb2

def run():
    with grpc.insecure_channel('localhost:{}'.format(common.PORT)) as channel:
        stub = adafruit_pb2_grpc.AHT20Stub(channel)
        response = stub.Measure(request=empty_pb2.Empty())
    print('Temperature: {}'.format(response.temperature))
    print('Relative Humidity: {}'.format(response.temperature))


if __name__ == '__main__':
    logging.basicConfig()
    run()
