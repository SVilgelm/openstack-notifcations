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
import functools
import logging

import grpc

import events
from pb import service_pb2_grpc


def stub(f):
    @functools.wraps(f)
    def wrapper(args):
        logging.debug('Request: %s', args)
        channel = grpc.insecure_channel(args.addrport)
        stub = service_pb2_grpc.ServiceStub(channel)
        res = f(stub, args)
        print res

    return wrapper


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Debug mode')
    parser.add_argument('--addrport', default='[::]:50051',
                        help='Optional ipaddr:port, default: [::]:50051')
    subparsers = parser.add_subparsers()
    parser_add_event = subparsers.add_parser('AddEvent')
    parser_add_event.add_argument('data', nargs='*')
    parser_add_event.set_defaults(func=stub(events.add_event))

    args = parser.parse_args()

    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    logging.basicConfig(level=level)
    logging.root.name = 'OpenStack Notifications'
    args.func(args)
