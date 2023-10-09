"""`GET`: `/api/v1/trace-list` endpoint configuration."""

from pydantic import BaseModel

from ._endpoint import Endpoint
from .resp_base import RespBase


class ReqTraceList(BaseModel):
    """`GET`: `/api/v1/trace-list` request model.

    Attributes:
        nids: The node ids to pull the `TraceMeta` for.
    """

    nids: list[str]


class TraceMeta(BaseModel):
    """A trace meta object. This is a lightweight object that contains the trace's metadata but excludes the data itself.

    Attributes:
        identifier: The trace's identifier.
        length: The trace's length.
    """

    identifier: str
    length: int


class RespTraceList(RespBase):
    """`GET`: `/api/v1/trace-list` response model.

    Attributes:
        traces: `dict[nid, dict[trace identifier, TraceMeta]]`.
    """

    traces: dict[str, dict[str, TraceMeta]]


end_trace_list = Endpoint("GET", "/trace-list", ReqTraceList, RespTraceList)
