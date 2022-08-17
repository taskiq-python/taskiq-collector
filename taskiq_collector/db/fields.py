import ormar


class JsonList(ormar.JSON):
    """
    JSON field for ormar models.

    This field overrides _sample parameter,
    so in schema you'll see an array.
    """

    _sample = [1, 2]  # type: ignore


class JsonDict(ormar.JSON):
    """
    JSON field for ormar models.

    This field overrides _sample parameter,
    so in schema you'll see a json object.
    """

    _sample = {"a": "b"}  # type: ignore
