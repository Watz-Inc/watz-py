"""`GET`: `/api/v1/ping` endpoint configuration."""

import typing_extensions as tp
from pydantic import BaseModel

from ._endpoint import Endpoint
from .resp_base import RespBase


class ReqPing(BaseModel):
    """`GET`: `/api/v1/ping` request model.

    No specific attributes.
    """

    pass


class RespPing(RespBase):
    """`GET`: `/api/v1/ping` response model.

    Attributes:
        status: Always `"OK"`.
        whoami: The researcher's email address attached to the token.
    """

    status: tp.Literal["OK"]
    whoami: str


end_ping = Endpoint("GET", "/ping", ReqPing, RespPing)
