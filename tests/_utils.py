import typing_extensions as tp
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

import watz

T = tp.TypeVar("T", bound=BaseModel)


def gen_mock_model(model: type[T], **overrides: tp.Any) -> T:
    """Create mock data for a model.

    Args:
        model: The model to create mock data for.
        **overrides: Specific fields of the model to concretely set.

    Returns:
        The model instanstiated with mock data.
    """

    class Factory(ModelFactory):
        __model__ = model

    return tp.cast(T, Factory.build(factory_use_construct=False, **overrides))


def fake_client() -> watz.Client:
    return watz.Client(secret="foo")  # nosec
