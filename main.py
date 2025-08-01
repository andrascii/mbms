import os
import asyncio
import logging
import grpc
import marzban_manager_pb2_grpc as proto_grpc

from server import Server
from config import Config
from common.setup_logger import setup_logger


async def main(config: Config):
    try:
        listen_addr = f"[::]:{config.grpc_port}"

        options = [('grpc.max_message_length', 300 * 1024 * 1024)]
        server = grpc.aio.server(options=options)
        server.add_insecure_port(listen_addr)
        manager = await Server.create(config=config)
        proto_grpc.add_MarzbanManagerServicer_to_server(manager, server)

        logging.info(f"Server will listen on {listen_addr}")

        await server.start()
        await server.wait_for_termination()

    except (asyncio.CancelledError, KeyboardInterrupt):
        logging.info("received shutdown signal")
        await server.stop(0)

    except Exception as e:
        logging.info(f"error occurred during processing: {e}")
        await server.stop(0)


if __name__ == "__main__":
    config = Config()

    log_level = logging.INFO

    if config.log_level.lower() == "debug":
        log_level = logging.DEBUG
    if config.log_level.lower() == "info":
        log_level = logging.INFO
    if config.log_level.lower() == "warning":
        log_level = logging.WARN
    if config.log_level.lower() == "error":
        log_level = logging.ERROR
    if config.log_level.lower() == "critical":
        log_level = logging.CRITICAL

    setup_logger(filename="mbms.log", level=log_level)

    try:
        asyncio.run(main(config=config))
    except KeyboardInterrupt:
        logging.info("Program interrupted by user")
