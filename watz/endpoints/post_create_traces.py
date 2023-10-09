"""`POST`: `/api/v1/traces` endpoint configuration."""

import typing as tp

from pydantic import BaseModel

from ._endpoint import Endpoint
from .resp_base import RespBase


class CreateTrace(BaseModel):
    """A creator model for a trace.

    Attributes:
        identifier: The trace's identifier, this must be unique.
        data: The list of json-compatible data.
    """

    identifier: str
    data: list[tp.Any]


class ReqCreateTraces(BaseModel):
    """`POST`: `/api/v1/traces` request model.

    Attributes:
        traces: A dict of node ids to a list of `CreateTrace` models for each respective node.
    """

    traces: dict[str, list[CreateTrace]]
    pass


class RespCreateTraces(RespBase):
    """`POST`: `/api/v1/traces` response model.

    No specific attributes.
    """

    pass


end_create_traces = Endpoint("POST", "/traces", ReqCreateTraces, RespCreateTraces)
