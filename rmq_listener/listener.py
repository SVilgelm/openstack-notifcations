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
import ConfigParser
import json
import logging
import pprint

import kombu


class PrettyLog(object):
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return pprint.pformat(self.obj)

    __str__ = __repr__


class Listener(object):

    def __init__(self, config):
        self.manager = config.get('manager', 'host')
        self.user = config.get('rabbit', 'username')
        self.password = config.get('rabbit', 'password')
        self.host = '%(host)s:%(port)s' % {
            'host': config.get('rabbit', 'host'),
            'port': config.get('rabbit', 'port')
        }

    @staticmethod
    def process_msg(message, amqp):
        try:
            logging.debug('%s', PrettyLog(json.loads(message)))
            # TODO: send message
        except Exception as e:
            logging.exception(e)

        amqp.ack()

    @property
    def queue(self):
        bindings = []
        for name in ('nova', 'cinder', 'neutron', 'glance', 'openstack'):
            exchange = kombu.Exchange(name, type='topic', durable=False)
            bindings.append(kombu.binding(exchange,
                                          routing_key='notifications.*'))
        return kombu.Queue('cedr_notifications', bindings=bindings,
                           durable=False)

    def listen(self):
        with kombu.Connection('amqp://{0}:{1}@{2}//'.format(
                self.user,
                self.password,
                self.host
        )) as conn:
            with conn.Consumer(queues=self.queue,
                               callbacks=[self.process_msg]):
                try:
                    while True:
                        conn.drain_events()
                except KeyboardInterrupt:
                    exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Debug mode')
    args = parser.parse_args()

    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    logging.basicConfig(level=level)

    config = ConfigParser.ConfigParser()
    config.read(args.config)

    listener = Listener(config)
    listener.listen()
