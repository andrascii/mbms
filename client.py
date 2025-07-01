# Copyright 2015 gRPC authors.
#
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
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging

import grpc
import asyncio
import marzban_manager_pb2 as proto
import marzban_manager_pb2_grpc as proto_grpc

from datetime import datetime, timedelta, timezone
from google.protobuf.json_format import MessageToDict

async def main():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    try:
        logging.info("Will try to add user...")

        channel = grpc.aio.insecure_channel("localhost:50051")
        stub = proto_grpc.MarzbanManagerStub(channel)

        inbounds = await stub.GetInbounds(
            proto.Empty()
        )

        create_user_request = proto.UserCreate(
            username="ADMIN",
            proxies={"vless": proto.ProxySettings(flow="xtls-rprx-vision")}
        )
        
        inbounds_dict = MessageToDict(inbounds)

        for k, v in inbounds_dict["inbounds"].items():
            for inbound in v["values"]:
                create_user_request.inbounds[k].values.append(inbound["tag"])

        response = await stub.AddUser(create_user_request)

        logging.info(f"client received:\n{response}")

        #response = await stub.GetUser(
        #    proto.GetUserRequest(
        #        username="594514115"
        #    )
        #)

        #logging.info(f"client received:\n{response}")
    except grpc.aio.AioRpcError as e:
        logging.error(f"gRPC error: {e.code()} - {e.details()}")

if __name__ == "__main__":
    logging.basicConfig(
        format='[%(asctime)s][%(name)s][%(levelname)s]: %(message)s',
        level=logging.INFO
    )

    logging.basicConfig()
    asyncio.run(main())
