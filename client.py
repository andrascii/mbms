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

import json
import grpc
import asyncio
import marzban_manager_pb2 as proto
import marzban_manager_pb2_grpc as proto_grpc

from datetime import datetime, timedelta, timezone
from google.protobuf.json_format import MessageToDict

async def add_user_example(stub: proto_grpc.MarzbanManagerStub, inbounds: proto.GetInboundsReply):
    create_user_request = proto.UserCreate(
        username="ADMIN",
        proxies={"vless": proto.ProxySettings(flow="xtls-rprx-vision")},
    )

    inbounds_dict = MessageToDict(inbounds)

    for k, v in inbounds_dict["inbounds"].items():
        for inbound in v["values"]:
            create_user_request.inbounds[k].values.append(inbound["tag"])

    return await stub.add_user(create_user_request)

async def update_user_example(stub: proto_grpc.MarzbanManagerStub):
    ...

async def get_user_example(stub: proto_grpc.MarzbanManagerStub, username: str) -> proto.UserResponse:
    return await stub.get_user(proto.GetUserRequest(username=username))

async def get_all_users_example(
    stub: proto_grpc.MarzbanManagerStub,
    username: str = None,
    offset: int = None,
    limit: int = None,
    search: str = None
) -> proto.GetAllUsersReply:
    return await stub.get_all_users(proto.GetAllUsersRequest(
        username=username,
        offset=offset,
        limit=limit,
        search=search
    ))

async def get_inbounds_example(stub: proto_grpc.MarzbanManagerStub):
    return await stub.get_inbounds(proto.Empty())


async def main():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    try:
        logging.info("Will try to add user...")

        channel = grpc.aio.insecure_channel("localhost:50051")
        stub = proto_grpc.MarzbanManagerStub(channel)

        response = add_user_example(stub)
        response = await get_user_example(stub, "594514115")
        logging.info(f"get user received:\n{response}")

        response = await get_all_users_example(
            stub,
            limit=500,
            offset=0
        )

        logging.info(f"got {len(response.users)} users")

    except grpc.aio.AioRpcError as e:
        logging.error(f"gRPC error: {e.code()} - {e.details()}")


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s", level=logging.INFO
    )

    logging.basicConfig()
    asyncio.run(main())
