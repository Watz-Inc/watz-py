# Conversions

Most standard types are serialized to json and back without modification:

- `bool`
- `int`
- `float`
- `str`
- `NoneType`
- `list`
- `dict`

The following types are supported, but serialize to json-compatible types destructively:

| Python Type                      | Json Type | Example Input                       | Example Output                | Notes                                                                                 |
| -------------------------------- | --------- | ----------------------------------- | ----------------------------- | ------------------------------------------------------------------------------------- |
| `decimal.Decimal`                | `float`   | `Decimal("13.14")`                  | `13.14`                       |                                                                                       |
| `datetime.datetime`              | `str`     | `time(12, 0, 0)`                    | `"12:00:00"`                  |                                                                                       |
| `datetime.date`                  | `str`     | `date(2021, 1, 1)`                  | `"2021-01-01"`                |                                                                                       |
| `datetime.time`                  | `str`     | `datetime(2021, 1, 1)`              | `"2021-01-01T00:00:00+00:00"` | [RFC 3339](https://tools.ietf.org/html/rfc3339) format, compatible with `isoformat()` |
| `datetime.timedelta`             | `float`   | `timedelta(days=1, milliseconds=1)` | `86400.001`                   | Total seconds                                                                         |
| `np.array`                       | `list`    | `np.array([1, 2, 3])`               | `[1, 2, 3]`                   |                                                                                       |
| `set`                            | `list`    | `{"a", "b", "c"}`                   | `["a", "b", "c"]`             |                                                                                       |
| `tuple`                          | `list`    | `(1, 2, 3)`                         | `[1, 2, 3]`                   |                                                                                       |
| `dataclasses.dataclass`          | `dict`    | `Model(a=11, b="12")`               | `{'a': 11, 'b': '12'}`        |                                                                                       |
| `pydantic.dataclasses.dataclass` | `dict`    | `Model(a=11, b="12")`               | `{'a': 11, 'b': '12'}`        |                                                                                       |
| `pydantic.BaseModel`             | `dict`    | `Model(a=11, b="12")`               | `{'a': 11, 'b': '12'}`        |                                                                                       |
