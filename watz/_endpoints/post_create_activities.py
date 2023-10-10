"""`POST`: `/api/v1/activities` endpoint configuration."""

from pydantic import BaseModel

from ._endpoint import Endpoint
from .get_subjects import Activity
from .resp_base import RespBase


class NewActivity(BaseModel):
    """A creator model for an activity.

    Attributes:
        label: An optional label for the activity. If omitted, the label will default to the auto-generated uid.
    """

    label: str


class ReqCreateActivities(BaseModel):
    """`POST`: `/api/v1/activities` request model.

    Attributes:
        activities: A list of activities to create.
    """

    activities: list[NewActivity]


class RespCreateActivities(RespBase):
    """`POST`: `/api/v1/activities` response model.

    Attributes:
        activities: The created activity models, in the same order they were supplied.
    """

    activities: list[Activity]


end_create_activities = Endpoint("POST", "/activities", ReqCreateActivities, RespCreateActivities)
