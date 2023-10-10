import re

import typing_extensions as tp
from pydantic import BaseModel
from pytest_httpx import HTTPXMock

from tests import _utils as ut
from watz._endpoints.get_ping import end_ping
from watz._endpoints.get_subjects import end_subjects
from watz._endpoints.get_trace_data import end_trace_data
from watz._endpoints.get_trace_list import end_trace_list
from watz._endpoints.post_create_activities import NewActivity, end_create_activities
from watz._endpoints.post_create_subjects import NewSubject, end_create_subjects
from watz._endpoints.post_create_traces import NewTrace, end_create_traces

T = tp.TypeVar("T", bound=BaseModel)


def test_endpoints(httpx_mock: HTTPXMock):
    eps = [
        end_ping,
        end_subjects,
        end_trace_data,
        end_trace_list,
        end_create_subjects,
        end_create_activities,
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
    assert isinstance(client.subjects(), end_subjects.resp_model)
    assert isinstance(client.trace_data({"123": ["sd", "df"]}), end_trace_data.resp_model)
    assert isinstance(client.trace_list(["1", "a"]), end_trace_list.resp_model)
    assert isinstance(
        client.create_subjects([NewSubject(uid="foo@foo.com"), NewSubject(uid="bar@bar.com")]),
        end_create_subjects.resp_model,
    )
    assert isinstance(
        client.create_activities([NewActivity(label="foo"), NewActivity(label="bar")]),
        end_create_activities.resp_model,
    )
    assert isinstance(
        client.create_traces(
            {
                "123": [
                    NewTrace(
                        uid="foo",
                        data=[{"x": 1, "y": 2}, 1, 2, 3, True, False],
                    )
                ]
            }
        ),
        end_create_traces.resp_model,
    )
