"""`GET`: `/api/v1/node-map` endpoint configuration."""

import typing_extensions as tp
from pydantic import BaseModel

from ._endpoint import Endpoint
from .resp_base import RespBase


class ReqNodeMap(BaseModel):
    """`GET`: `/api/v1/node-map` request model.

    Attributes:
        root_pk: The root node's id to build the map from. If `None`, the root node is
            assumed to be the calling user's root node.
    """

    root_nid: tp.Optional[str]


class NodeBase(BaseModel):
    """The base node model.

    Attributes:
        nid: The node's id.
        label: The node's label.
    """

    nid: str
    label: str


class ActivityNode(NodeBase):
    """An activity node. Labels are non-unique. When no custom label, this nodes label defaults to the nid."""


class UserNode(NodeBase):
    """A user node. Labels are unique. A user node's label is always the user's email address.

    Attributes:
        activities: The node's relating activity nodes (if any).
        subjects: The node's subjects' user nodes (if the user is a researcher).
    """

    activities: list[ActivityNode]
    subjects: list["UserNode"]


class RespNodeMap(RespBase):
    """`GET`: `/api/v1/node-map` response model.

    Attributes:
        node: The root node, matching the node id given in the request.
    """

    node: UserNode


end_node_map = Endpoint(
    "GET",
    "/node-map",
    ReqNodeMap,
    RespNodeMap,
    # Generator cause recursion error for some reason, override:
    resp_example=lambda: RespNodeMap(
        node=UserNode(
            nid="foo",
            label="foo",
            activities=[
                ActivityNode(nid="foo", label="foo"),
                ActivityNode(nid="foo", label="foo"),
            ],
            subjects=[
                UserNode(
                    nid="foo",
                    label="e1@bar.com",
                    activities=[ActivityNode(nid="foo", label="foo")],
                    subjects=[UserNode(nid="foo", label="e2@bar.com", activities=[], subjects=[])],
                )
            ],
        )
    ),
)
