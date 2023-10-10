"""`POST`: `/api/v1/traces` endpoint configuration."""

import typing as tp

from pydantic import BaseModel

from ._endpoint import Endpoint
from .resp_base import RespBase


class NewTrace(BaseModel):
    """A creator model for a trace.

    Attributes:
        uid: The trace's identifier, this must be unique to the subject/activity.
        data: The list of json-compatible data.
    """

    uid: str
    data: list[tp.Any]


class ReqCreateTraces(BaseModel):
    """`POST`: `/api/v1/traces` request model.

    Attributes:
        traces: A dict of activity/subject uids to a list of `NewTrace` models for each respective activity/subject.
    """

    traces: dict[str, list[NewTrace]]
    pass


class RespCreateTraces(RespBase):
    """`POST`: `/api/v1/traces` response model.

    No specific attributes.
    """

    pass


end_create_traces = Endpoint("POST", "/traces", ReqCreateTraces, RespCreateTraces)
