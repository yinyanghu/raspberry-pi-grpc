from grpc_tools import protoc

protoc.main((
    '',
    '-I../proto',
    '-I/usr/local/include',
    '--python_out=.',
    '--grpc_python_out=.',
    '../proto/adafruit.proto',
))