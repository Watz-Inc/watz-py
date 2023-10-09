import time
import warnings
from typing import Optional

import httpx
import typing_extensions as tp
from pydantic import BaseModel, ValidationError

from .resp_base import RespBase

Req_T = tp.TypeVar("Req_T", bound=BaseModel)
Resp_T = tp.TypeVar("Resp_T", bound=RespBase)
Method_T = tp.TypeVar("Method_T", bound=tp.Literal["GET", "POST", "PUT", "DELETE"])

CONN_WAIT_SECS = 0.5


class Endpoint(tp.Generic[Method_T, Req_T, Resp_T]):
    method: Method_T
    req_model: type[Req_T]
    resp_model: type[Resp_T]
    path: str

    # For testing:
    _resp_example: tp.Optional[tp.Callable[[], Resp_T]] = None

    def __init__(
        self,
        method: Method_T,
        path: str,
        req_model: type[Req_T],
        resp_model: type[Resp_T],
        resp_example: Optional[tp.Optional[tp.Callable[[], Resp_T]]] = None,
    ):
        self.req_model = req_model
        self.resp_model = resp_model
        self.method = method
        self.path = path
        self._resp_example = resp_example

    def call(self, session: httpx.Client, req: Req_T) -> Resp_T:
        resp = self._req(session, req)
        return self._parse(resp)

    def _req(self, session: httpx.Client, req: Req_T) -> httpx.Response:
        for x in range(5):
            try:
                return session.request(
                    self.method,
                    self.path,
                    params=req.model_dump() if self.method == "GET" else None,
                    json=req.model_dump_json() if self.method != "GET" else None,
                )
            except httpx.ConnectError:
                warnings.warn(
                    "Failed to connect to Watz API. Attempt {} of 5.".format(x + 1), stacklevel=3
                )
            time.sleep(CONN_WAIT_SECS)

        raise httpx.ConnectError("Failed to connect to Watz API after 5 attempts.")

    def _parse(self, resp: httpx.Response) -> Resp_T:
        resp.raise_for_status()
        try:
            return self.resp_model.model_validate_json(resp.text)
        except ValidationError as e:
            raise ValueError(
                "Unexpected data structure from Watz API.\n{}".format(resp.json())
            ) from e
