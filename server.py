import os
import grpc
import logging
import httpx
import marzban
from functools import wraps
from marzban import MarzbanAPI
from typing import Callable, Awaitable, Any

import marzban_manager_pb2 as proto
import marzban_manager_pb2_grpc as proto_grpc

from google.protobuf.json_format import MessageToDict

from environments import ENV_MB_PANEL_URL, ENV_MB_PANEL_USER, ENV_MB_PANEL_PASSWORD


def to_proto_status(status: str) -> proto.Status:
    if status == "active":
        return proto.Status.ACTIVE
    if status == "on_hold":
        return proto.Status.ON_HOLD
    if status == "expired":
        return proto.Status.EXPIRED
    if status == "disabled":
        return proto.Status.DISABLED
    if status == "limited":
        return proto.Status.LIMITED
    raise ValueError(f"Unknown status: {status}")


def proto_status_to_str(status: proto.Status) -> str:
    if status == proto.Status.ACTIVE:
        return "active"
    if status == proto.Status.ON_HOLD:
        return "on_hold"
    if status == proto.Status.DISABLED:
        return "disabled"
    if status == proto.Status.EXPIRED:
        return "expired"
    if status == proto.Status.LIMITED:
        return "limited"
    raise ValueError(f"Unknown status: {status}")


def to_proto_data_limit_reset_strategy(strategy: str) -> proto.DataLimitResetStrategy:
    if strategy == "no_reset":
        return proto.DataLimitResetStrategy.NO_RESET
    if strategy == "day":
        return proto.DataLimitResetStrategy.DAY
    if strategy == "week":
        return proto.DataLimitResetStrategy.WEEK
    if strategy == "month":
        return proto.DataLimitResetStrategy.MONTH
    if strategy == "year":
        return proto.DataLimitResetStrategy.YEAR
    raise ValueError(f"Unknown data limit reset strategy: {strategy}")


def proto_data_limit_reset_strategy_to_str(
    strategy: proto.DataLimitResetStrategy,
) -> str:
    if strategy == proto.DataLimitResetStrategy.NO_RESET:
        return "no_reset"
    if strategy == proto.DataLimitResetStrategy.DAY:
        return "day"
    if strategy == proto.DataLimitResetStrategy.WEEK:
        return "week"
    if strategy == proto.DataLimitResetStrategy.MONTH:
        return "month"
    if strategy == proto.DataLimitResetStrategy.YEAR:
        return "year"
    raise ValueError(f"Unknown data limit reset strategy: {strategy}")


def to_proto_user_response(user: marzban.UserResponse) -> proto.UserResponse:
    proto_user = proto.UserResponse()
    if user.username is not None:
        proto_user.username = user.username

    if user.proxies:
        for key, proxy in user.proxies.items():
            p = proto.ProxySettings()
            if proxy.id is not None:
                p.id = proxy.id

            if proxy.flow is not None:
                p.flow = proxy.flow

            proto_user.proxies[key].CopyFrom(p)

    if user.expire is not None:
        proto_user.expire = user.expire

    if user.data_limit is not None:
        proto_user.data_limit = user.data_limit

    if user.data_limit_reset_strategy is not None:
        proto_user.data_limit_reset_strategy = to_proto_data_limit_reset_strategy(
            user.data_limit_reset_strategy
        )

    if user.inbounds:
        for key, inbound_list in user.inbounds.items():
            inbound_proto_list = proto.InboundList()
            inbound_proto_list.values.extend(inbound_list)
            proto_user.inbounds[key].CopyFrom(inbound_proto_list)

    if user.note is not None:
        proto_user.note = user.note

    if user.sub_updated_at is not None:
        proto_user.sub_updated_at = user.sub_updated_at

    if user.sub_last_user_agent is not None:
        proto_user.sub_last_user_agent = user.sub_last_user_agent

    if user.online_at is not None:
        proto_user.online_at = user.online_at

    if user.on_hold_expire_duration is not None:
        proto_user.on_hold_expire_duration = user.on_hold_expire_duration

    if user.on_hold_timeout is not None:
        proto_user.on_hold_timeout = user.on_hold_timeout

    if user.status is not None:
        proto_user.status = to_proto_status(user.status)

    if user.used_traffic is not None:
        proto_user.used_traffic = user.used_traffic

    if user.lifetime_used_traffic is not None:
        proto_user.lifetime_used_traffic = user.lifetime_used_traffic

    if user.links:
        proto_user.links.extend(user.links)

    if user.subscription_url is not None:
        proto_user.subscription_url = user.subscription_url

    if user.subscription_token is not None:
        proto_user.subscription_token = user.subscription_token

    if user.excluded_inbounds:
        for key, excluded_list in user.excluded_inbounds.items():
            excl_proto_list = proto.InboundList()
            excl_proto_list.values.extend(excluded_list)
            proto_user.excluded_inbounds[key].CopyFrom(excl_proto_list)

    if user.next_plan is not None:
        np = proto.NextPlan()
        np.add_remaining_traffic = user.next_plan.add_remaining_traffic

        if user.next_plan.data_limit is not None:
            np.data_limit = user.next_plan.data_limit

        if user.next_plan.expire is not None:
            np.expire = user.next_plan.expire

        np.fire_on_either = user.next_plan.fire_on_either
        proto_user.next_plan.CopyFrom(np)

    if user.admin is not None:
        admin = proto.AdminInfo()
        admin.username = user.admin.username
        admin.is_sudo = user.admin.is_sudo

        if user.admin.telegram_id is not None:
            admin.telegram_id = user.admin.telegram_id

        if user.admin.discord_webhook is not None:
            admin.discord_webhook = user.admin.discord_webhook

        if user.admin.users_usage is not None:
            admin.users_usage = user.admin.users_usage

        proto_user.admin.CopyFrom(admin)

    if user.created_at is not None:
        proto_user.created_at = user.created_at

    return proto_user


def _to_marzban_user(object, marzban_class):
    return marzban_class(
        # у UserModify может не быть username
        username=getattr(object, "username", None),
        proxies=(
            {
                k: marzban.ProxySettings(**MessageToDict(v))
                for k, v in object.proxies.items()
            }
            if object.proxies
            else {}
        ),
        expire=object.expire if object.HasField("expire") else None,
        data_limit=object.data_limit if object.HasField("data_limit") else None,
        data_limit_reset_strategy=(
            to_proto_data_limit_reset_strategy(object.data_limit_reset_strategy)
            if object.HasField("data_limit_reset_strategy")
            else None
        ),
        inbounds=(
            {k: v.values for k, v in object.inbounds.items()} if object.inbounds else {}
        ),
        note=object.note if object.HasField("note") else None,
        sub_updated_at=(
            object.sub_updated_at if object.HasField("sub_updated_at") else None
        ),
        sub_last_user_agent=(
            object.sub_last_user_agent
            if object.HasField("sub_last_user_agent")
            else None
        ),
        online_at=object.online_at if object.HasField("online_at") else None,
        on_hold_expire_duration=(
            object.on_hold_expire_duration
            if object.HasField("on_hold_expire_duration")
            else None
        ),
        on_hold_timeout=(
            object.on_hold_timeout if object.HasField("on_hold_timeout") else None
        ),
        status=proto_status_to_str(object.status) if object.HasField("status") else None,
        next_plan=(
            marzban.NextPlanModel(**MessageToDict(object.next_plan))
            if object.HasField("next_plan")
            else None
        ),
    )


def to_marzban_user_create(object: proto.UserCreate) -> marzban.UserCreate:
    return _to_marzban_user(object, marzban.UserCreate)


def to_marzban_user_modify(object: proto.UserModify) -> marzban.UserModify:
    return _to_marzban_user(object, marzban.UserModify)


class Server(proto_grpc.MarzbanManager):
    def __init__(self, api: MarzbanAPI, token: marzban.Token):
        super().__init__()
        self.__api = api
        self.__token = token

    def __retry_on_unauthorized(func: Callable[..., Awaitable[Any]]):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                return await func(self, *args, **kwargs)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    logging.warning("Unauthorized request, refreshing token")
                    await self._refresh_token()
                    return await func(self, *args, **kwargs)
                raise

        return wrapper

    async def _refresh_token(self):
        """
        Refresh the token using the Marzban API.
        """
        _, mb_panel_user, mb_panel_password = Server.__get_env()

        self.__token = await self.__api.get_token(
            username=mb_panel_user, password=mb_panel_password
        )

        if not self.__token:
            raise ValueError("Failed to get token from the panel")

    @classmethod
    def __get_env(cls) -> tuple[str, str, str]:
        mb_panel_url = os.getenv(ENV_MB_PANEL_URL)
        mb_panel_user = os.getenv(ENV_MB_PANEL_USER)
        mb_panel_password = os.getenv(ENV_MB_PANEL_PASSWORD)

        if not mb_panel_url:
            raise ValueError(f"{ENV_MB_PANEL_URL} environment variable is not set")

        if not mb_panel_user:
            raise ValueError(f"{ENV_MB_PANEL_USER} environment variable is not set")

        if not mb_panel_password:
            raise ValueError(f"{ENV_MB_PANEL_PASSWORD} environment variable is not set")

        return (mb_panel_url, mb_panel_user, mb_panel_password)

    @classmethod
    async def create(cls):
        mb_panel_url, mb_panel_user, mb_panel_password = cls.__get_env()

        api = MarzbanAPI(base_url=mb_panel_url)
        token = await api.get_token(username=mb_panel_user, password=mb_panel_password)

        if not token:
            raise ValueError("Failed to get token from the panel")

        return cls(api, token)

    async def add_user(
        self, request: proto.UserCreate, context: grpc.aio.ServicerContext
    ) -> proto.UserResponse:
        try:
            logging.info(f"{__name__} for {request.username}")

            if not request.inbounds:
                details = f"Failed to add user '{request.username}': inbounds empty"
                logging.error(details)
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(details)
                return proto.UserResponse()

            if not request.proxies:
                details = f"Failed to add user '{request.username}': proxies empty"
                logging.error(details)
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(details)
                return proto.UserResponse()

            response = await self.__api_add_user(request)
            return to_proto_user_response(response)
        except httpx.HTTPStatusError as e:
            logging.error(f"Failed to add user: {e}")
            if e.response.status_code == 409:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details(f"User {request.username} already exists")
            else:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"User {request.username} could not be added: {e}")
            return proto.UserResponse()
        except httpx.HTTPError as e:
            logging.error(f"Failed to add user: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to add user: {request.username}")
            return proto.UserResponse()

    async def update_user(
        self, request: proto.UpdateUserRequest, context: grpc.aio.ServicerContext
    ) -> proto.UpdateUserReply:
        try:
            logging.info(f"{__name__} for {request.username}")
            response = await self.__api_modify_user(request)
            return proto.UpdateUserReply(user=to_proto_user_response(response))
        except httpx.HTTPError as e:
            logging.error(f"Failed to update user: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to update user: {request.username}")
            return proto.UpdateUserReply()

    async def get_user(
        self, request: proto.GetUserRequest, context: grpc.aio.ServicerContext
    ) -> proto.UserResponse:
        try:
            logging.info(f"{__name__} for {request.username}")
            response = await self.__api_get_user(request)
            return to_proto_user_response(response)
        except httpx.HTTPError as e:
            logging.error(f"Failed to fetch user: {e}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User not found: {request.username}")
            return proto.UserResponse()

    async def get_all_users(
        self, request: proto.GetAllUsersRequest, context: grpc.aio.ServicerContext
    ) -> proto.GetAllUsersReply:
        try:
            logging.info(f"{__name__} for {request}")
            all_users = await self.__api_get_all_users(request)
            reply = proto.GetAllUsersReply(total=all_users.total)
            proto_user_list: list[proto.UserResponse] = [
                to_proto_user_response(user)
                for user in all_users.users
            ]
            reply.users.extend(proto_user_list)
            return reply
        except httpx.HTTPError as e:
            details = f"Failed to get all users: {e}"
            logging.error(details)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(details)
            return proto.GetInboundsReply()

    async def get_inbounds(
        self, request: proto.Empty, context: grpc.aio.ServicerContext
    ) -> proto.GetInboundsReply:
        try:
            logging.info(__name__)
            inbounds = await self.__api_get_inbounds(request)

            return proto.GetInboundsReply(
                inbounds={
                    key: proto.ProxyInboundList(
                        values=[
                            proto.ProxyInbound(
                                tag=inb["tag"],
                                protocol=inb["protocol"],
                                network=inb["network"],
                                tls=inb["tls"],
                                port=str(inb["port"]),
                            )
                            for inb in inbound_list
                        ]
                    )
                    for key, inbound_list in inbounds.items()
                }
            )
        except httpx.HTTPError as e:
            logging.error(f"Failed to get inbounds: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to get inbounds: {e}")
            return proto.GetInboundsReply()

    @__retry_on_unauthorized
    async def __api_add_user(self, request: proto.UserCreate) -> marzban.UserResponse:
        logging.debug(f"{__name__} called for {request}")
        user_create = to_marzban_user_create(request)
        return await self.__api.add_user(
            user=user_create, token=self.__token.access_token
        )

    @__retry_on_unauthorized
    async def __api_modify_user(
        self, request: proto.UpdateUserRequest
    ) -> marzban.UserResponse:
        logging.debug(f"{__name__} called for {request}")

        user_modify = to_marzban_user_modify(request.update)
        logging.debug(f"user modify JSON: {user_modify.model_dump(exclude_none=True)}")

        return await self.__api.modify_user(
            username=request.username,
            user=user_modify,
            token=self.__token.access_token,
        )

    @__retry_on_unauthorized
    async def __api_get_user(
        self, request: proto.GetUserRequest
    ) -> marzban.UserResponse:
        logging.debug(f"{__name__} called for {request}")
        return await self.__api.get_user(
            username=request.username, token=self.__token.access_token
        )

    @__retry_on_unauthorized
    async def __api_get_all_users(
        self, request: proto.GetAllUsersRequest
    ) -> marzban.UsersResponse:
        logging.debug(f"{__name__} called for {request}")
        return await self.__api.get_users(
            offset=request.offset if request.HasField("offset") else None,
            limit=request.limit if request.HasField("limit") else None,
            username=request.username if request.HasField("username") else None,
            search=request.search if request.HasField("search") else None,
            token=self.__token.access_token,
        )
    
    @__retry_on_unauthorized
    async def __api_get_inbounds(self, request: proto.Empty):
        return await self.__api.get_inbounds(token=self.__token.access_token)
