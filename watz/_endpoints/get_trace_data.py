"""`GET`: `/api/v1/trace-data` endpoint configuration."""

import typing as tp

from pydantic import BaseModel

from ._endpoint import Endpoint
from .get_trace_list import TraceMeta
from .resp_base import RespBase


class ReqTraceData(BaseModel):
    """`GET`: `/api/v1/trace-data` request model.

    Attributes:
        traces: A dict of subject/activity uids to a list of trace uids for each respective subject/activity.
    """

    traces: dict[str, list[str]]


class TraceData(TraceMeta):
    """An extended `TraceMeta` object that contains the trace's data.

    Attributes:
        data: The list of json-compatible data.
    """

    data: list[tp.Any]


class RespTraceData(RespBase):
    """`GET`: `/api/v1/trace-data` response model.

    Attributes:
        traces: `dict[subject/act uid, dict[trace uid, TraceData]]`.
    """

    traces: dict[str, dict[str, tp.Optional[TraceData]]]


end_trace_data = Endpoint("GET", "/trace-data", ReqTraceData, RespTraceData)
