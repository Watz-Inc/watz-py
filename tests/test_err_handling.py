import httpx
import pytest
from pytest_httpx import HTTPXMock

import watz
import watz._endpoints._endpoint
from tests import _utils as ut


def test_err_unexpected_response(httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="GET", json="Invalid")
    client = ut.fake_client()
    with pytest.raises(ValueError, match="Unexpected data structure from Watz API.\nInvalid"):
        client.ping()


def test_err_api_unavail(httpx_mock: HTTPXMock):
    before_val = watz._endpoints._endpoint.CONN_WAIT_SECS
    try:
        watz._endpoints._endpoint.CONN_WAIT_SECS = 0
        client = ut.fake_client()
        httpx_mock.add_exception(httpx.ConnectError("No connect"))
        with pytest.raises(
            httpx.ConnectError, match="Failed to connect to Watz API after 5 attempts."
        ):
            client.ping()
    finally:
        watz._endpoints._endpoint.CONN_WAIT_SECS = before_val
