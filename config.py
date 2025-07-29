import os

MB_MS_LOG_LEVEL = "MB_MS_LOG_LEVEL"
MB_MS_PANEL_URL = "MB_MS_PANEL_URL"
MB_MS_PANEL_USER = "MB_MS_PANEL_USER"
MB_MS_PANEL_PASSWORD = "MB_MS_PANEL_PASSWORD"
MB_MS_GRPC_PORT = "MB_MS_GRPC_PORT"


class Config:
    def __init__(self):
        self.log_level: str = os.getenv(MB_MS_LOG_LEVEL)

        if not self.log_level:
            self.log_level = "info"

        self.grpc_port = os.getenv(MB_MS_GRPC_PORT)

        if not self.grpc_port:
            raise ValueError(f"environment variable {MB_MS_GRPC_PORT} was not set")
        
        self.marzban_panel_url = os.getenv(MB_MS_PANEL_URL)

        if not self.marzban_panel_url:
            raise ValueError(f"environment variable {MB_MS_PANEL_URL} was not set")
        
        self.marzban_panel_user = os.getenv(MB_MS_PANEL_USER)

        if not self.marzban_panel_user:
            raise ValueError(f"environment variable {MB_MS_PANEL_USER} was not set")
        
        self.marzban_panel_password = os.getenv(MB_MS_PANEL_PASSWORD)

        if not self.marzban_panel_password:
            raise ValueError(f"environment variable {MB_MS_PANEL_PASSWORD} was not set")
