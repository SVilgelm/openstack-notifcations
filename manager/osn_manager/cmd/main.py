#!/usr/bin/env python

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from concurrent import futures
import logging
import os
import time

import grpc

from osn_manager.pb import service_pb2_grpc
from osn_manager import server

_ONE_DAY_IN_SECONDS = 24 * 60 * 60


def is_true(value):
    return value.lower() in ('1', 'on', 'y', 'yes', 'true', 't')


def serve(addrport):
    srv = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ServiceServicer_to_server(server.Server(), srv)
    srv.add_insecure_port(addrport)
    srv.start()
    logging.getLogger(__name__).info('Running on %s', addrport)
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        srv.stop(0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Debug mode')
    parser.add_argument('addrport', nargs='?', default='[::]:50051',
                        help='Optional ipaddr:port, default: [::]:50051')
    args = parser.parse_args()

    level = logging.INFO
    if args.debug or is_true(os.environ.get('DEBUG', '')):
        level = logging.DEBUG
    logging.basicConfig(level=level)
    logging.root.name = 'OpenStack Notifications'
    serve(args.addrport)


if __name__ == '__main__':
    main()
