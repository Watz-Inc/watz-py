"""`GET`: `/api/v1/trace-list` endpoint configuration."""

from pydantic import BaseModel

from ._endpoint import Endpoint
from .resp_base import RespBase


class ReqTraceList(BaseModel):
    """`GET`: `/api/v1/trace-list` request model.

    Attributes:
        uids: The subject/activity uids to pull the `TraceMeta` for.
    """

    uids: list[str]


class TraceMeta(BaseModel):
    """A trace meta object. This is a lightweight object that contains the trace's metadata but excludes the data itself.

    Attributes:
        uid: The trace's unique identifier.
        length: The trace's length.
    """

    uid: str
    length: int


class RespTraceList(RespBase):
    """`GET`: `/api/v1/trace-list` response model.

    Attributes:
        traces: `dict[subject/act uid, dict[trace uid, TraceMeta]]`.
    """

    traces: dict[str, dict[str, TraceMeta]]


end_trace_list = Endpoint("GET", "/trace-list", ReqTraceList, RespTraceList)
