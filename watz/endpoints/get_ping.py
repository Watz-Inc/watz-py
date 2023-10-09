"""`GET`: `/api/v1/ping` endpoint configuration."""

import typing_extensions as tp
from pydantic import BaseModel

from ._endpoint import Endpoint
from .resp_base import RespBase


class ReqPing(BaseModel):
    """`GET`: `/api/v1/ping` request model.

    No parameters.
    """

    pass


class RespPing(RespBase):
    """`GET`: `/api/v1/ping` response model.

    Attributes:
        status: Always `"OK"`.
        whoami: The user's email address attached to the token.
        root_nid: The calling user's root node id.
    """

    status: tp.Literal["OK"]
    whoami: str
    root_nid: str


end_ping = Endpoint("GET", "/ping", ReqPing, RespPing)
