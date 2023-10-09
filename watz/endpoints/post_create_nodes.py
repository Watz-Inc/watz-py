"""`POST`: `/api/v1/nodes` endpoint configuration."""

import typing_extensions as tp
from pydantic import BaseModel

from ._endpoint import Endpoint
from .resp_base import RespBase


class CreateActivityNode(BaseModel):
    """A creator model for an activity node.

    Attributes:
        parent_nid: The parent node id.
        label: The label for the node, if left as `None` will default to the created nid for the node.
    """

    parent_nid: str
    label: tp.Optional[str]


class CreateUserNode(BaseModel):
    """A creator model for a user node.

    Attributes:
        parent_nid: The parent node id.
        label: The label for the node, must be a valid, unique email address for the user.
    """

    parent_nid: str
    label: str


class ReqCreateNodes(BaseModel):
    """`POST`: `/api/v1/nodes` request model.

    Attributes:
        nodes: A list of nodes to create, either `CreateActivityNode` or `CreateUserNode` models.
    """

    nodes: list[tp.Union[CreateActivityNode, CreateUserNode]]


class RespCreateNodes(RespBase):
    """`POST`: `/api/v1/nodes` response model.

    Attributes:
        nids: The list of created node ids in the same order they were given in the request.
    """

    nids: list[str]


end_create_nodes = Endpoint("POST", "/nodes", ReqCreateNodes, RespCreateNodes)
