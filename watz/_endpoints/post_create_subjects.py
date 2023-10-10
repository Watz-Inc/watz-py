"""`POST`: `/api/v1/subjects` endpoint configuration."""

from pydantic import BaseModel

from ._endpoint import Endpoint
from .resp_base import RespBase


class NewSubject(BaseModel):
    """A creator model for a subject.

    Attributes:
        uid: The unique identifier for the subject. Currently, this must be a valid email address.
    """

    uid: str


class ReqCreateSubjects(BaseModel):
    """`POST`: `/api/v1/subjects` request model.

    Attributes:
        subjects: A list of subjects to create.
    """

    subjects: list[NewSubject]


class RespCreateSubjects(RespBase):
    """`POST`: `/api/v1/subjects` response model.

    No specific attributes.
    """

    pass


end_create_subjects = Endpoint("POST", "/subjects", ReqCreateSubjects, RespCreateSubjects)
