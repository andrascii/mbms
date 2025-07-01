import json
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

from environments import (
    ENV_MB_PANEL_URL,
    ENV_MB_PANEL_USER,
    ENV_MB_PANEL_PASSWORD
)


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


def proto_data_limit_reset_strategy_to_str(strategy: proto.DataLimitResetStrategy) -> str:
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


def to_proto_user_response(
    user: marzban.UserResponse
) -> proto.UserResponse:
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
            user.data_limit_reset_strategy)

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
        proxies={
            k: marzban.ProxySettings(**MessageToDict(v)) for k, v in object.proxies.items()
        } if object.proxies else {},
        expire=object.expire or None,
        data_limit=object.data_limit or None,
        data_limit_reset_strategy=object.data_limit_reset_strategy or "no_reset",
        inbounds={
            k: v.values for k, v in object.inbounds.items()
        } if object.inbounds else {},
        note=object.note or None,
        sub_updated_at=object.sub_updated_at or None,
        sub_last_user_agent=object.sub_last_user_agent or None,
        online_at=object.online_at or None,
        on_hold_expire_duration=object.on_hold_expire_duration or None,
        on_hold_timeout=object.on_hold_timeout or None,
        status=object.status or "active",
        next_plan=marzban.NextPlanModel(
            **MessageToDict(object.next_plan)
        ) if object.HasField("next_plan") else None,
    )


def to_marzban_user_create(object: proto.UserCreate) -> marzban.UserCreate:
    return _to_marzban_user(object, marzban.UserCreate)


def to_marzban_user_modify(object: proto.UserModify) -> marzban.UserModify:
    return _to_marzban_user(object, marzban.UserModify)


class MarzbanManager(proto_grpc.MarzbanManager):
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
                    self.__token = await self._RefreshToken()
                    return await func(self, *args, **kwargs)
                raise
        return wrapper
    
    async def _RefreshToken(self):
        """
        Refresh the token using the Marzban API.
        """
        _, mb_panel_user, mb_panel_password = MarzbanManager.__GetEnv()

        self.__token = await self.__api.get_token(username=mb_panel_user, password=mb_panel_password)

        if not self.__token:
            raise ValueError("Failed to get token from the panel")

    @classmethod
    def __GetEnv(cls) -> tuple[str, str, str]:
        mb_panel_url = os.getenv(ENV_MB_PANEL_URL)
        mb_panel_user = os.getenv(ENV_MB_PANEL_USER)
        mb_panel_password = os.getenv(ENV_MB_PANEL_PASSWORD)

        if not mb_panel_url:
            raise ValueError(f'{ENV_MB_PANEL_URL} environment variable is not set')

        if not mb_panel_user:
            raise ValueError(f'{ENV_MB_PANEL_USER} environment variable is not set')

        if not mb_panel_password:
            raise ValueError(f'{ENV_MB_PANEL_PASSWORD} environment variable is not set')

        return (mb_panel_url, mb_panel_user, mb_panel_password)

    @classmethod
    async def Create(cls):
        mb_panel_url, mb_panel_user, mb_panel_password = cls.__GetEnv()

        api = MarzbanAPI(base_url=mb_panel_url)
        token = await api.get_token(username=mb_panel_user, password=mb_panel_password)

        if not token:
            raise ValueError("Failed to get token from the panel")

        return cls(api, token)


    @__retry_on_unauthorized
    async def AddUser(
        self,
        request: proto.UserCreate,
        context: grpc.aio.ServicerContext
    ) -> proto.UserResponse:
        try:
            logging.info(f"Adding user: {request.username}")

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

            user_create = to_marzban_user_create(request)

            user_response = await self.__api.add_user(
                user=user_create,
                token=self.__token.access_token
            )
            return to_proto_user_response(user_response)
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


    @__retry_on_unauthorized
    async def UpdateUser(
        self,
        request: proto.UpdateUserRequest,
        context: grpc.aio.ServicerContext
    ) -> proto.UpdateUserReply:
        try:
            logging.info(f"Updating user: {request.username}")
            user_modify = to_marzban_user_modify(request.user)
            user_response = await self.__api.modify_user(
                username=request.username,
                user=user_modify,
                token=self.__token.access_token
            )
            return proto.UpdateUserReply(user=to_proto_user_response(user_response))
        except httpx.HTTPError as e:
            logging.error(f"Failed to update user: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to update user: {request.username}")
            return proto.UpdateUserReply()


    @__retry_on_unauthorized
    async def GetUser(
        self,
        request: proto.GetUserRequest,
        context: grpc.aio.ServicerContext
    ) -> proto.UserResponse:
        try:
            logging.info(f"Fetching user: {request.username}")
            return to_proto_user_response(await self.__api.get_user(
                username=request.username,
                token=self.__token.access_token
            ))
        except httpx.HTTPError as e:
            logging.error(f"Failed to fetch user: {e}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"User not found: {request.username}")
            return proto.UserResponse()
        

    @__retry_on_unauthorized
    async def GetInbounds(
        self,
        request: proto.Empty,
        context: grpc.aio.ServicerContext
    ) -> proto.GetInboundsReply:
        try:
            logging.info("Getting inbounds")
            inbounds = await self.__api.get_inbounds(token=self.__token.access_token)

            return proto.GetInboundsReply(
                inbounds={
                    key: proto.ProxyInboundList(
                        values=[
                            proto.ProxyInbound(
                                tag=inb["tag"],
                                protocol=inb["protocol"],
                                network=inb["network"],
                                tls=inb["tls"],
                                port=str(inb["port"])
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
