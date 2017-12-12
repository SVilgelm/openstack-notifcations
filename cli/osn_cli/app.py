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
import logging
import os
import sys

from cliff import app
from cliff import commandmanager
import grpc

from osn_cli.pb import service_pb2_grpc


def is_true(value):
    return value.lower() in ('1', 'on', 'y', 'yes', 'true', 't')


class CLIApp(app.App):
    def __init__(self):
        super(CLIApp, self).__init__(
            description='OpenStack Notifications Command Line Interface',
            version='1.0',
            command_manager=commandmanager.CommandManager('osn'),
            deferred_help=True,
        )
        self.stub = None

    def build_option_parser(self, description, version, argparse_kwargs=None):
        argparse_kwargs = argparse_kwargs or {}
        parser = argparse.ArgumentParser(
            description=description,
            add_help=False,
            **argparse_kwargs
        )
        if self.deferred_help:
            parser.add_argument(
                '-h', '--help',
                dest='deferred_help',
                action='store_true',
                help="Show help message and exit.",
            )
        else:
            parser.add_argument(
                '-h', '--help',
                action=help.HelpAction,
                nargs=0,
                default=self,  # tricky
                help="Show help message and exit.",
            )
        parser.add_argument('-d', '--debug',
                            action='store_true', help='Debug mode.')
        parser.add_argument('--addrport', default='[::]:50051',
                            help='Optional ipaddr:port, default: [::]:50051')
        return parser

    def configure_logging(self):
        level = logging.INFO
        if self.options.debug or is_true(os.environ.get('DEBUG', '')):
            level = logging.DEBUG
        logging.basicConfig(level=level)
        # logging.root.name = 'OpenStack Notifications'

    def initialize_app(self, argv):
        self.LOG.debug('Connecting to %s', self.options.addrport)
        channel = grpc.insecure_channel(self.options.addrport)
        self.stub = service_pb2_grpc.ServiceStub(channel)

    def prepare_to_run_command(self, cmd):
        cmd.stub = self.stub

    def clean_up(self, cmd, result, err):
        if err:
            self.LOG.debug('Got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = CLIApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main())
