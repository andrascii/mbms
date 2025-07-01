from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataLimitResetStrategy(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_RESET: _ClassVar[DataLimitResetStrategy]
    DAY: _ClassVar[DataLimitResetStrategy]
    WEEK: _ClassVar[DataLimitResetStrategy]
    MONTH: _ClassVar[DataLimitResetStrategy]
    YEAR: _ClassVar[DataLimitResetStrategy]

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTIVE: _ClassVar[Status]
    DISABLED: _ClassVar[Status]
    LIMITED: _ClassVar[Status]
    EXPIRED: _ClassVar[Status]
    ON_HOLD: _ClassVar[Status]

NO_RESET: DataLimitResetStrategy
DAY: DataLimitResetStrategy
WEEK: DataLimitResetStrategy
MONTH: DataLimitResetStrategy
YEAR: DataLimitResetStrategy
ACTIVE: Status
DISABLED: Status
LIMITED: Status
EXPIRED: Status
ON_HOLD: Status

class ProxySettings(_message.Message):
    __slots__ = ("id", "flow")
    ID_FIELD_NUMBER: _ClassVar[int]
    FLOW_FIELD_NUMBER: _ClassVar[int]
    id: str
    flow: str
    def __init__(
        self, id: _Optional[str] = ..., flow: _Optional[str] = ...
    ) -> None: ...

class NextPlan(_message.Message):
    __slots__ = ("add_remaining_traffic", "data_limit", "expire", "fire_on_either")
    ADD_REMAINING_TRAFFIC_FIELD_NUMBER: _ClassVar[int]
    DATA_LIMIT_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_FIELD_NUMBER: _ClassVar[int]
    FIRE_ON_EITHER_FIELD_NUMBER: _ClassVar[int]
    add_remaining_traffic: bool
    data_limit: int
    expire: int
    fire_on_either: bool
    def __init__(
        self,
        add_remaining_traffic: bool = ...,
        data_limit: _Optional[int] = ...,
        expire: _Optional[int] = ...,
        fire_on_either: bool = ...,
    ) -> None: ...

class AdminInfo(_message.Message):
    __slots__ = ("username", "is_sudo", "telegram_id", "discord_webhook", "users_usage")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    IS_SUDO_FIELD_NUMBER: _ClassVar[int]
    TELEGRAM_ID_FIELD_NUMBER: _ClassVar[int]
    DISCORD_WEBHOOK_FIELD_NUMBER: _ClassVar[int]
    USERS_USAGE_FIELD_NUMBER: _ClassVar[int]
    username: str
    is_sudo: bool
    telegram_id: int
    discord_webhook: str
    users_usage: int
    def __init__(
        self,
        username: _Optional[str] = ...,
        is_sudo: bool = ...,
        telegram_id: _Optional[int] = ...,
        discord_webhook: _Optional[str] = ...,
        users_usage: _Optional[int] = ...,
    ) -> None: ...

class InboundList(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, values: _Optional[_Iterable[str]] = ...) -> None: ...

class UserResponse(_message.Message):
    __slots__ = (
        "username",
        "proxies",
        "expire",
        "data_limit",
        "data_limit_reset_strategy",
        "inbounds",
        "note",
        "sub_updated_at",
        "sub_last_user_agent",
        "online_at",
        "on_hold_expire_duration",
        "on_hold_timeout",
        "status",
        "used_traffic",
        "lifetime_used_traffic",
        "links",
        "subscription_url",
        "subscription_token",
        "excluded_inbounds",
        "next_plan",
        "admin",
        "created_at",
    )

    class ProxiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProxySettings
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[ProxySettings, _Mapping]] = ...,
        ) -> None: ...

    class InboundsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: InboundList
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[InboundList, _Mapping]] = ...,
        ) -> None: ...

    class ExcludedInboundsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: InboundList
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[InboundList, _Mapping]] = ...,
        ) -> None: ...

    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PROXIES_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_FIELD_NUMBER: _ClassVar[int]
    DATA_LIMIT_FIELD_NUMBER: _ClassVar[int]
    DATA_LIMIT_RESET_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    INBOUNDS_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    SUB_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SUB_LAST_USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    ONLINE_AT_FIELD_NUMBER: _ClassVar[int]
    ON_HOLD_EXPIRE_DURATION_FIELD_NUMBER: _ClassVar[int]
    ON_HOLD_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    USED_TRAFFIC_FIELD_NUMBER: _ClassVar[int]
    LIFETIME_USED_TRAFFIC_FIELD_NUMBER: _ClassVar[int]
    LINKS_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_URL_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIPTION_TOKEN_FIELD_NUMBER: _ClassVar[int]
    EXCLUDED_INBOUNDS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PLAN_FIELD_NUMBER: _ClassVar[int]
    ADMIN_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    username: str
    proxies: _containers.MessageMap[str, ProxySettings]
    expire: int
    data_limit: int
    data_limit_reset_strategy: DataLimitResetStrategy
    inbounds: _containers.MessageMap[str, InboundList]
    note: str
    sub_updated_at: str
    sub_last_user_agent: str
    online_at: str
    on_hold_expire_duration: int
    on_hold_timeout: str
    status: Status
    used_traffic: int
    lifetime_used_traffic: int
    links: _containers.RepeatedScalarFieldContainer[str]
    subscription_url: str
    subscription_token: str
    excluded_inbounds: _containers.MessageMap[str, InboundList]
    next_plan: NextPlan
    admin: AdminInfo
    created_at: str
    def __init__(
        self,
        username: _Optional[str] = ...,
        proxies: _Optional[_Mapping[str, ProxySettings]] = ...,
        expire: _Optional[int] = ...,
        data_limit: _Optional[int] = ...,
        data_limit_reset_strategy: _Optional[_Union[DataLimitResetStrategy, str]] = ...,
        inbounds: _Optional[_Mapping[str, InboundList]] = ...,
        note: _Optional[str] = ...,
        sub_updated_at: _Optional[str] = ...,
        sub_last_user_agent: _Optional[str] = ...,
        online_at: _Optional[str] = ...,
        on_hold_expire_duration: _Optional[int] = ...,
        on_hold_timeout: _Optional[str] = ...,
        status: _Optional[_Union[Status, str]] = ...,
        used_traffic: _Optional[int] = ...,
        lifetime_used_traffic: _Optional[int] = ...,
        links: _Optional[_Iterable[str]] = ...,
        subscription_url: _Optional[str] = ...,
        subscription_token: _Optional[str] = ...,
        excluded_inbounds: _Optional[_Mapping[str, InboundList]] = ...,
        next_plan: _Optional[_Union[NextPlan, _Mapping]] = ...,
        admin: _Optional[_Union[AdminInfo, _Mapping]] = ...,
        created_at: _Optional[str] = ...,
    ) -> None: ...

class UserCreate(_message.Message):
    __slots__ = (
        "username",
        "proxies",
        "expire",
        "data_limit",
        "data_limit_reset_strategy",
        "inbounds",
        "note",
        "sub_updated_at",
        "sub_last_user_agent",
        "online_at",
        "on_hold_expire_duration",
        "on_hold_timeout",
        "status",
        "next_plan",
    )

    class ProxiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProxySettings
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[ProxySettings, _Mapping]] = ...,
        ) -> None: ...

    class InboundsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: InboundList
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[InboundList, _Mapping]] = ...,
        ) -> None: ...

    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PROXIES_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_FIELD_NUMBER: _ClassVar[int]
    DATA_LIMIT_FIELD_NUMBER: _ClassVar[int]
    DATA_LIMIT_RESET_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    INBOUNDS_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    SUB_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SUB_LAST_USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    ONLINE_AT_FIELD_NUMBER: _ClassVar[int]
    ON_HOLD_EXPIRE_DURATION_FIELD_NUMBER: _ClassVar[int]
    ON_HOLD_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PLAN_FIELD_NUMBER: _ClassVar[int]
    username: str
    proxies: _containers.MessageMap[str, ProxySettings]
    expire: int
    data_limit: int
    data_limit_reset_strategy: DataLimitResetStrategy
    inbounds: _containers.MessageMap[str, InboundList]
    note: str
    sub_updated_at: str
    sub_last_user_agent: str
    online_at: str
    on_hold_expire_duration: int
    on_hold_timeout: str
    status: Status
    next_plan: NextPlan
    def __init__(
        self,
        username: _Optional[str] = ...,
        proxies: _Optional[_Mapping[str, ProxySettings]] = ...,
        expire: _Optional[int] = ...,
        data_limit: _Optional[int] = ...,
        data_limit_reset_strategy: _Optional[_Union[DataLimitResetStrategy, str]] = ...,
        inbounds: _Optional[_Mapping[str, InboundList]] = ...,
        note: _Optional[str] = ...,
        sub_updated_at: _Optional[str] = ...,
        sub_last_user_agent: _Optional[str] = ...,
        online_at: _Optional[str] = ...,
        on_hold_expire_duration: _Optional[int] = ...,
        on_hold_timeout: _Optional[str] = ...,
        status: _Optional[_Union[Status, str]] = ...,
        next_plan: _Optional[_Union[NextPlan, _Mapping]] = ...,
    ) -> None: ...

class UserModify(_message.Message):
    __slots__ = (
        "proxies",
        "expire",
        "data_limit",
        "data_limit_reset_strategy",
        "inbounds",
        "note",
        "sub_updated_at",
        "sub_last_user_agent",
        "online_at",
        "on_hold_expire_duration",
        "on_hold_timeout",
        "status",
        "next_plan",
    )

    class ProxiesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProxySettings
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[ProxySettings, _Mapping]] = ...,
        ) -> None: ...

    class InboundsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: InboundList
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[InboundList, _Mapping]] = ...,
        ) -> None: ...

    PROXIES_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_FIELD_NUMBER: _ClassVar[int]
    DATA_LIMIT_FIELD_NUMBER: _ClassVar[int]
    DATA_LIMIT_RESET_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    INBOUNDS_FIELD_NUMBER: _ClassVar[int]
    NOTE_FIELD_NUMBER: _ClassVar[int]
    SUB_UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    SUB_LAST_USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    ONLINE_AT_FIELD_NUMBER: _ClassVar[int]
    ON_HOLD_EXPIRE_DURATION_FIELD_NUMBER: _ClassVar[int]
    ON_HOLD_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    NEXT_PLAN_FIELD_NUMBER: _ClassVar[int]
    proxies: _containers.MessageMap[str, ProxySettings]
    expire: int
    data_limit: int
    data_limit_reset_strategy: DataLimitResetStrategy
    inbounds: _containers.MessageMap[str, InboundList]
    note: str
    sub_updated_at: str
    sub_last_user_agent: str
    online_at: str
    on_hold_expire_duration: int
    on_hold_timeout: str
    status: Status
    next_plan: NextPlan
    def __init__(
        self,
        proxies: _Optional[_Mapping[str, ProxySettings]] = ...,
        expire: _Optional[int] = ...,
        data_limit: _Optional[int] = ...,
        data_limit_reset_strategy: _Optional[_Union[DataLimitResetStrategy, str]] = ...,
        inbounds: _Optional[_Mapping[str, InboundList]] = ...,
        note: _Optional[str] = ...,
        sub_updated_at: _Optional[str] = ...,
        sub_last_user_agent: _Optional[str] = ...,
        online_at: _Optional[str] = ...,
        on_hold_expire_duration: _Optional[int] = ...,
        on_hold_timeout: _Optional[str] = ...,
        status: _Optional[_Union[Status, str]] = ...,
        next_plan: _Optional[_Union[NextPlan, _Mapping]] = ...,
    ) -> None: ...

class UpdateUserRequest(_message.Message):
    __slots__ = ("username", "update")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_FIELD_NUMBER: _ClassVar[int]
    username: str
    update: UserModify
    def __init__(
        self,
        username: _Optional[str] = ...,
        update: _Optional[_Union[UserModify, _Mapping]] = ...,
    ) -> None: ...

class UpdateUserReply(_message.Message):
    __slots__ = ("user",)
    USER_FIELD_NUMBER: _ClassVar[int]
    user: UserResponse
    def __init__(
        self, user: _Optional[_Union[UserResponse, _Mapping]] = ...
    ) -> None: ...

class GetAllUsersRequest(_message.Message):
    __slots__ = ("offset", "limit")
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    offset: int
    limit: int
    def __init__(
        self, offset: _Optional[int] = ..., limit: _Optional[int] = ...
    ) -> None: ...

class GetAllUsersReply(_message.Message):
    __slots__ = ("users", "total")
    USERS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[UserResponse]
    total: int
    def __init__(
        self,
        users: _Optional[_Iterable[_Union[UserResponse, _Mapping]]] = ...,
        total: _Optional[int] = ...,
    ) -> None: ...

class GetUserRequest(_message.Message):
    __slots__ = ("username",)
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    username: str
    def __init__(self, username: _Optional[str] = ...) -> None: ...

class ProxyInbound(_message.Message):
    __slots__ = ("tag", "protocol", "network", "tls", "port")
    TAG_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    TLS_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    tag: str
    protocol: str
    network: str
    tls: str
    port: str
    def __init__(
        self,
        tag: _Optional[str] = ...,
        protocol: _Optional[str] = ...,
        network: _Optional[str] = ...,
        tls: _Optional[str] = ...,
        port: _Optional[str] = ...,
    ) -> None: ...

class ProxyInboundList(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[ProxyInbound]
    def __init__(
        self, values: _Optional[_Iterable[_Union[ProxyInbound, _Mapping]]] = ...
    ) -> None: ...

class GetInboundsReply(_message.Message):
    __slots__ = ("inbounds",)

    class InboundsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ProxyInboundList
        def __init__(
            self,
            key: _Optional[str] = ...,
            value: _Optional[_Union[ProxyInboundList, _Mapping]] = ...,
        ) -> None: ...

    INBOUNDS_FIELD_NUMBER: _ClassVar[int]
    inbounds: _containers.MessageMap[str, ProxyInboundList]
    def __init__(
        self, inbounds: _Optional[_Mapping[str, ProxyInboundList]] = ...
    ) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
