"""`GET`: `/api/v1/trace-data` endpoint configuration."""

import typing as tp

from pydantic import BaseModel

from ._endpoint import Endpoint
from .get_trace_list import TraceMeta
from .resp_base import RespBase


class ReqTraceData(BaseModel):
    """`GET`: `/api/v1/trace-data` request model.

    Attributes:
        traces: A dict of node ids to a list of trace identifiers for each respective node.
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
        traces: `dict[nid, dict[trace identifier, TraceData | None]]`. The trace will be `None` when the trace does not exist.
    """

    traces: dict[str, dict[str, tp.Optional[TraceData]]]


end_trace_data = Endpoint("GET", "/trace-data", ReqTraceData, RespTraceData)
