"""The central API client."""

from functools import cached_property
from typing import Optional

import typing_extensions as tp

from ._client_base import ClientBase
from .endpoints.get_node_map import ReqNodeMap, RespNodeMap, end_node_map
from .endpoints.get_ping import ReqPing, RespPing, end_ping
from .endpoints.get_trace_data import ReqTraceData, RespTraceData, end_trace_data
from .endpoints.get_trace_list import ReqTraceList, RespTraceList, end_trace_list
from .endpoints.post_create_nodes import (
    CreateActivityNode,
    CreateUserNode,
    ReqCreateNodes,
    RespCreateNodes,
    end_create_nodes,
)
from .endpoints.post_create_traces import (
    CreateTrace,
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

    @cached_property
    def root_nid(self) -> str:
        """The root node's id for the calling user. This is retrieved from a `ping()` on creation and cached thereafter.

        Returns:
            str: The root node's id.
        """
        return self.ping().root_nid

    def ping(self) -> RespPing:
        """Ping the API.

        Returns:
            RespPing
        """
        return end_ping.call(self._session, ReqPing())

    def node_map(self, root_nid: Optional[tp.Optional[str]] = None) -> RespNodeMap:
        """Retrieve the structure of nodes accessible to the caller.

        Args:
            root_nid (tp.Optional[str], optional): The root node's id to build the map from. If `None`, the root node is assumed to be the calling user's root node, stored from a `ping()` on creation.

        Returns:
            RespNodeMap
        """
        return end_node_map.call(self._session, ReqNodeMap(root_nid=root_nid or self.root_nid))

    def trace_list(self, nids: tp.Iterable[str]) -> RespTraceList:
        """Retrieves the trace metadata for the requested nodes.

        Args:
            nids (list[str]): The node ids to retrieve trace metadata for.

        Returns:
            RespTraceList
        """
        return end_trace_list.call(
            self._session,
            ReqTraceList(
                nids=tp.cast(list[str], nids)  # Pydantic can handle the conversion if needed.
            ),
        )

    def trace_data(self, traces: tp.Mapping[str, tp.Iterable[str]]) -> RespTraceData:
        """Retrieves the trace data for the request traces.

        Args:
            traces (dict[str, list[str]]): A dict of node ids to a list of trace identifiers for each respective node.

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

    def create_nodes(
        self, nodes: tp.Iterable[tp.Union[CreateActivityNode, CreateUserNode]]
    ) -> RespCreateNodes:
        """Creates new nodes.

        Args:
            nodes (list[tp.Union[CreateActivityNode, CreateUserNode]]): The nodes to create.

        Returns:
            RespCreateNodes
        """
        return end_create_nodes.call(
            self._session,
            ReqCreateNodes(
                nodes=tp.cast(  # Pydantic can handle the conversion if needed.
                    list[tp.Union[CreateActivityNode, CreateUserNode]], nodes
                )
            ),
        )

    def create_traces(self, traces: tp.Mapping[str, tp.Iterable[CreateTrace]]) -> RespCreateTraces:
        """Creates new traces.

        Args:
            traces (dict[str, tp.Iterable[CreateTrace]]): A dict of node ids to a list of traces to create for each respective node.

        Returns:
            RespCreateTraces
        """
        return end_create_traces.call(
            self._session,
            ReqCreateTraces(
                traces=tp.cast(  # Pydantic can handle the conversion if needed.
                    dict[str, list[CreateTrace]], traces
                )
            ),
        )
