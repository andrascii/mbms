import os
import asyncio
import logging
import grpc
import marzban_manager_pb2_grpc as proto_grpc

from server import Server
from environments import ENV_MB_MS_GRPC_PORT

logger = logging.getLogger(__name__)


async def main():
    grpc_server_port = os.getenv(ENV_MB_MS_GRPC_PORT)

    if not grpc_server_port:
        raise ValueError(f"environment variable {ENV_MB_MS_GRPC_PORT} was not set")

    listen_addr = f"[::]:{grpc_server_port}"

    server = grpc.aio.server()
    server.add_insecure_port(listen_addr)
    manager = await Server.create()
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
