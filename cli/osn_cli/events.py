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

import logging
import sys

from osn_cli import common
from osn_cli.pb import event_pb2


class Event(common.Lister):
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Event, self).get_parser(prog_name)
        parser.add_argument('data', nargs='*',
                            help='List of events or - to read from stdin')
        return parser

    @staticmethod
    def data(data):
        if data and data[0] == '-':
            data = [sys.stdin.read()]
        return iter(event_pb2.RawData(data=d) for d in data)

    def take_action(self, parsed_args):
        self.log.debug(list(parsed_args.data))
        response = self.stub.AddEvent(self.data(parsed_args.data))

        def res():
            for r in response:
                yield (r.id, )

        return ('ID',), res()
