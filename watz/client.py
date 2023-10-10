"""The central API client."""

from typing import Optional

import typing_extensions as tp

from ._client_base import ClientBase
from ._endpoints.get_ping import ReqPing, RespPing, end_ping
from ._endpoints.get_subjects import ReqSubjects, RespSubjects, end_subjects
from ._endpoints.get_trace_data import ReqTraceData, RespTraceData, end_trace_data
from ._endpoints.get_trace_list import ReqTraceList, RespTraceList, end_trace_list
from ._endpoints.post_create_activities import (
    NewActivity,
    ReqCreateActivities,
    RespCreateActivities,
    end_create_activities,
)
from ._endpoints.post_create_subjects import (
    NewSubject,
    ReqCreateSubjects,
    RespCreateSubjects,
    end_create_subjects,
)
from ._endpoints.post_create_traces import (
    NewTrace,
    ReqCreateTraces,
    RespCreateTraces,
    end_create_traces,
)


class Client(ClientBase):
    """The central API client."""

    def __init__(
        self,
        base: str = "https://watz.coach",
        secret: Optional[tp.Optional[str]] = None,
    ):
        """Instantiates a new client.

        Args:
            base (str, optional): The base URL of the Watz API.
            secret (tp.Optional[str], optional): The API key. If omitted, will be read from the WATZ_SECRET environment variable.
        """
        super().__init__(base=base, secret=secret, version=1)

    def ping(self) -> RespPing:
        """Availability check. Pings the API.

        Returns:
            RespPing
        """
        return end_ping.call(self._session, ReqPing())

    def subjects(self) -> RespSubjects:
        """Retrieve the caller's subjects.

        Returns:
            RespSubjects
        """
        return end_subjects.call(self._session, ReqSubjects())

    def trace_list(self, uids: tp.Iterable[str]) -> RespTraceList:
        """Retrieves the trace metadata for the requested subjects/activities.

        Args:
            uids (tp.Iterable[str]): The subject/activity uids to retrieve trace metadata for.

        Returns:
            RespTraceList
        """
        return end_trace_list.call(
            self._session,
            ReqTraceList(
                uids=tp.cast(list[str], uids)  # Pydantic can handle the conversion if needed.
            ),
        )

    def trace_data(self, traces: tp.Mapping[str, tp.Iterable[str]]) -> RespTraceData:
        """Retrieves the trace data for the request traces.

        Args:
            traces (tp.Mapping[str, tp.Iterable[str]]): A dict of subject/activity uids to a list of trace identifiers for each respective subject/activity.

        Returns:
            RespTraceData
        """
        return end_trace_data.call(
            self._session,
            ReqTraceData(
                traces=tp.cast(  # Pydantic can handle the conversion if needed.
                    dict[str, list[str]], traces
                ),
            ),
        )

    def create_subjects(self, subjects: tp.Iterable[NewSubject]) -> RespCreateSubjects:
        """Create new subjects.

        Args:
            subjects (tp.Iterable[NewSubject]): The subjects to create.

        Returns:
            RespCreateSubjects
        """
        return end_create_subjects.call(
            self._session,
            ReqCreateSubjects(
                subjects=tp.cast(  # Pydantic can handle the conversion if needed.
                    list[NewSubject], subjects
                )
            ),
        )

    def create_activities(self, activities: tp.Iterable[NewActivity]) -> RespCreateActivities:
        """Create new activities.

        Args:
            activities (tp.Iterable[NewActivity]): The activities to create.

        Returns:
            RespCreateActivities
        """
        return end_create_activities.call(
            self._session,
            ReqCreateActivities(
                activities=tp.cast(  # Pydantic can handle the conversion if needed.
                    list[NewActivity], activities
                )
            ),
        )

    def create_traces(self, traces: tp.Mapping[str, tp.Iterable[NewTrace]]) -> RespCreateTraces:
        """Create new traces.

        Args:
            traces (tp.Mapping[str, tp.Iterable[NewTrace]]): A dict of subject/activity uids to a list of `NewTrace` models to create for each respective subject/activity.

        Returns:
            RespCreateTraces
        """
        return end_create_traces.call(
            self._session,
            ReqCreateTraces(
                traces=tp.cast(  # Pydantic can handle the conversion if needed.
                    dict[str, list[NewTrace]], traces
                )
            ),
        )
