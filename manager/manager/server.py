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
import uuid

from pb import event_pb2
from pb import service_pb2_grpc


class Server(service_pb2_grpc.ServiceServicer):
    def AddEvent(self, request, context):
        for r in request:
            logging.debug('AddEvent: data=%s', r.data)
            new_id = uuid.uuid4()
            yield event_pb2.ID(id=str(new_id))
