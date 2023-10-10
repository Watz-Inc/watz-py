"""`GET`: `/api/v1/subjects` endpoint configuration."""

from pydantic import BaseModel

from ._endpoint import Endpoint
from .resp_base import RespBase


class ReqSubjects(BaseModel):
    """`GET`: `/api/v1/subjects` request model.

    No specific attributes.
    """

    pass


class Activity(BaseModel):
    """An activity of a subject.

    Attributes:
        uid: The activity's unique id.
        label: The activity's label, if no label was provided this will default to the uid.
    """

    uid: str
    label: str


class Subject(BaseModel):
    """A subject of a researcher.

    Attributes:
        uid: The subject's unique id. Currently, this is always the subject's email address.
        activities: The subject's activities.
    """

    uid: str
    activities: list[Activity]


class RespSubjects(RespBase):
    """`GET`: `/api/v1/subjects` response model.

    Attributes:
        subjects: The subjects of the researcher.
    """

    subjects: list[Subject]


end_subjects = Endpoint("GET", "/subjects", ReqSubjects, RespSubjects)
