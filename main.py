import os
import asyncio
import logging
import grpc
import marzban_manager_pb2_grpc as proto_grpc

from server import Server
from config import Config

logger = logging.getLogger(__name__)


async def main():
    config = Config()

    listen_addr = f"[::]:{config.grpc_port}"

    server = grpc.aio.server()
    server.add_insecure_port(listen_addr)
    manager = await Server.create(config=config)
    proto_grpc.add_MarzbanManagerServicer_to_server(manager, server)

    logging.info(f"Server will listen on {listen_addr}")

    await server.start()

    try:
        await server.wait_for_termination()
    except (asyncio.CancelledError, KeyboardInterrupt):
        logging.info("Received shutdown signal")
        await server.stop(0)


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s][%(name)s][%(levelname)s]: %(message)s", level=logging.INFO
    )

    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Program interrupted by user")
