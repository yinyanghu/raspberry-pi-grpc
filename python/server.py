from concurrent import futures
import logging

import adafruit_ahtx0
import board
import grpc

import adafruit_pb2
import adafruit_pb2_grpc
import common

class AHT20Service(adafruit_pb2_grpc.AHT20Servicer):
    def __init__(self):
        self.sensor = adafruit_ahtx0.AHTx0(board.I2C())

    def Measure(self, request, context):
        return adafruit_pb2.AHT20Reply(
            temperature=self.sensor.temperature,
            relative_humidity=self.sensor.relative_humidity)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    adafruit_pb2_grpc.add_AHT20Servicer_to_server(AHT20Service(), server)
    server.add_insecure_port('[::]:{}'.format(common.PORT))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()