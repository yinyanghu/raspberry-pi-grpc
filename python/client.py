import ipaddress
import logging
import socket
import sys

import argparse
import grpc

import adafruit_pb2
import adafruit_pb2_grpc
import common
from google.protobuf import empty_pb2
import version

log = logging.getLogger('raspberry-pi-grpc-client')
log.setLevel(logging.WARNING)


def fetch(server):
    logging.info("connecting to server %s", server)
    with grpc.insecure_channel('{}:{}'.format(server, common.PORT)) as channel:
        stub = adafruit_pb2_grpc.AHT20Stub(channel)
        return stub.Measure(request=empty_pb2.Empty())


def get_server_address(server):
    try:
        return ipaddress.ip_address(server)
    except ValueError:
        logging.info("trying to find ip address by hostname %s", server)
        return socket.gethostbyname(server)


def output(data, args):
    if args.temperature or not args.relative_humidity:
        print(data.temperature if args.raw else 'Temperature: {:.2f}°C'.format(
            data.temperature))
    if args.relative_humidity or not args.temperature:
        print(data.relative_humidity if args.raw else 'Relative Humidity: {:.2f}%'.format(
            data.relative_humidity))


def main():
    parser = argparse.ArgumentParser(
        prog='raspberry-pi-grpc-client',
        description='A gRPC client for Raspberry Pi.'
    )
    parser.add_argument('--version', action='version',
                        version='%(prog)s {0}'.format(version.__version__),
                        help='print the version of raspberry-pi-grpc client and exit')
    parser.add_argument('server', help='hostname or ip address of server')

    parser.add_argument('--raw', action='store_true',
                        default=False, help='only output raw numbers')

    sensor_group = parser.add_mutually_exclusive_group()
    sensor_group.add_argument('-t', '--temperature', action='store_true',
                              default=False, help='only output temperature')
    sensor_group.add_argument('-r', '--relative-humidity', action='store_true',
                              default=False, help='only output relative humidity')

    args = parser.parse_args()

    data = fetch(get_server_address(args.server))

    output(data, args)


if __name__ == '__main__':
    main()
