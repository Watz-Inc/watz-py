"""The shared base response model returned from all endpoints."""

from pydantic import BaseModel, Field


class RespBase(BaseModel):
    """The base response model for all API endpoints.

    Attributes:
        warnings: Warnings returned that did not fail the request, but should be noted.
    """

    warnings: list[str] = Field(default_factory=list)
