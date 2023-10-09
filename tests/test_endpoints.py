import re

import typing_extensions as tp
from pydantic import BaseModel
from pytest_httpx import HTTPXMock

from tests import _utils as ut
from watz.endpoints.get_node_map import end_node_map
from watz.endpoints.get_ping import end_ping
from watz.endpoints.get_trace_data import end_trace_data
from watz.endpoints.get_trace_list import end_trace_list
from watz.endpoints.post_create_nodes import CreateActivityNode, CreateUserNode, end_create_nodes
from watz.endpoints.post_create_traces import CreateTrace, end_create_traces

T = tp.TypeVar("T", bound=BaseModel)


def test_endpoints(httpx_mock: HTTPXMock):
    eps = [
        end_ping,
        end_node_map,
        end_trace_data,
        end_trace_list,
        end_create_nodes,
        end_create_traces,
    ]

    for end in eps:
        example_model = (
            end._resp_example() if end._resp_example else ut.gen_mock_model(end.resp_model)
        )
        httpx_mock.add_response(
            method=end.method,
            url=re.compile(
                r"https://watz.coach/api/v1/" + re.escape(end.path.strip("/")) + r"/?\??"
            ),
            json=example_model.model_dump(),
        )

    client = ut.fake_client()

    assert isinstance(client.ping(), end_ping.resp_model)
    assert isinstance(client.node_map(), end_node_map.resp_model)
    assert isinstance(client.trace_data({"123": ["sd", "df"]}), end_trace_data.resp_model)
    assert isinstance(client.trace_list(["1", "a"]), end_trace_list.resp_model)
    assert isinstance(
        client.create_nodes(
            [
                CreateUserNode(parent_nid=client.root_nid, label="foo@bar.com"),
                CreateActivityNode(parent_nid=client.root_nid, label="foo"),
            ]
        ),
        end_create_nodes.resp_model,
    )
    assert isinstance(
        client.create_traces(
            {
                "123": [
                    CreateTrace(
                        identifier="foo",
                        data=[{"x": 1, "y": 2}, 1, 2, 3, True, False],
                    )
                ]
            }
        ),
        end_create_traces.resp_model,
    )
