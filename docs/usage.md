## Initializing the Client

To use the Watz API you need to obtain a key. See the API section on the [Watz website](https://watz.coach/docs/api) for details.

```py title="Inline secret"
import watz

client = watz.Client(secret="your api key")
```

Alternatively, a [`Client`][watz.Client] can read the api key from the environment variable `WATZ_SECRET`.

```py title="Secret from environment variable"
import os

os.environ["WATZ_SECRET"] = "your api key"
client = watz.Client()
```

!!! info
    Each call made with the [`Client`][watz.Client] is atomic. If something is invalid about the request, an exception will be raised and no changes will be made.

## Creating Subjects

A subject is an individual whom data can be assigned to. These subjects can be identified by their `uid`, currently always their email address.

Subjects are created with a [`NewSubject`][watz.models.NewSubject] model, and return a [`Subject`][watz.models.Subject].

```py title="Creating subjects"
client.subject_create(
    [
        watz.models.NewSubject(email="bar@bar.com"),
        watz.models.NewSubject(email="foo@foo.com"),
    ]
)
"""
[
    Subject(
        uid="bar@bar.com",
        email="bar@bar.com",
        activities=[],
    ),
    Subject(
        uid="foo@foo.com",
        email="foo@foo.com",
        activities=[],
    ),
]
"""
```

## Creating Activities

An activity is a specific event in time for a given subject, where data can be grouped together.

To create an activity, the only requirement is a `subject_uid` of a previously created subject. Currently, the `subject_uid` will always be the user's email address and can be accessed from `subject.uid` of a `Subject` model.

Activities are created with a [`NewActivity`][watz.models.NewActivity] model, and return an [`Activity`][watz.models.Activity].

Activities can be passed some optional parameters too:

| Parameter Name | Default          | Description                                                                                               |
| -------------- | ---------------- | --------------------------------------------------------------------------------------------------------  |
| `label`        | `"No label"`     | This label is attached to all [`Activity`][watz.models.Activity] objects, and can help identify activities|
| `start_time`   | `datetime.now()` | This marks the start of the specific activity                                                             |
| `fit_files`    | `[]`             | Fit files in the form of `bytes` will be parsed and used to automatically create traces for the activity  |

```py title="Creating activities"
import os
import datetime as dt

with open("fit_file.fit", "rb") as f:
    fit_file = f.read()

client.activity_create(
    [
        watz.models.NewActivity(subject_uid="bar@bar.com"),
        watz.models.NewActivity(
            subject_uid="foo@foo.com",
            label="foo",
            start_time=dt.datetime(2021, 1, 1),
            fit_files=[fit_file],
        ),
    ]
)
"""
[
    Activity(
        uid="act_1_uid", label="No Label", start_time=dt.datetime.now()
    ),
    Activity(
        uid="act_2_uid", label="foo", start_time=dt.datetime(2021, 1, 1)
    ),
]
"""
```

## Listing Subjects & Activities

The [`Client`][watz.Client] can be used to list existing subjects and activities in the system.

```py title="Listing subjects & activities"
client.subject_list()
"""
[
    Subject(
        uid="bar@bar.com",
        email="bar@bar.com",
        activities=[
            Activity(
                uid="act_1_uid",
                label="No Label",
                start_time=dt.datetime.now(),
            )
        ],
    ),
    Subject(
        uid="foo@foo.com",
        email="foo@foo.com",
        activities=[
            Activity(
                uid="act_2_uid",
                label="foo",
                start_time=dt.datetime(2021, 1, 1),
            )
        ],
    ),
]
"""
```

## Creating Traces

A trace is a store of arbitrary, json-serializable data that are attached to a subject or activity parent.

Traces are identified by their `name` and `parser_id`, which must be unique for the given subject/activity parent.

Traces are created with a [`NewTrace`][watz.models.NewTrace] model, and return a [`Trace`][watz.models.Trace].

!!! info
    Whilst traces are stored as json, they can be passed some custom python types, which will be serialized to valid json.
    E.g. `datetime`, `numpy.array([])` and pydantic models. The full list of data conversions can be found on the [Conversions Page](conversions.md).

```py title="Creating traces"
import datetime as dt
from pydantic import BaseModel

class ExamplePdModel(BaseModel):
    a: int
    b: str

client.trace_create(
    [
        watz.models.NewTrace(
            # Assigning to the subject "bar@bar.com"
            parent_uid="bar@bar.com",
            name="measurements",
            data={
                "height": 180,
                "weight": 80,
            },
        ),
        watz.models.NewTrace(
            # Assigning to the activity of the subject "foo@foo.com"
            parent_uid="act_2_uid",
            name="misc",
            data=[
                # See the full list of supported types on the Conversions Page
                1,
                "2",
                True,
                None,
                ["list"],
                {"dict": "nested"},
                (4, 5, 6),
                dt.datetime(2021, 1, 1),
                ExamplePdModel(a=11, b="12"),
            ],
        ),
    ]
)
"""
[
    Trace(uid="123", name="measurements", parser_id=2),
    Trace(uid="678", name="misc", parser_id=2),
]
"""
```

!!! info
    `parser_id` is implicit. It's used to identify how that data entered the system. For manual inputs, it's always `2`, for e.g. fit file generated traces, it's `3`.

## Retrieving Traces

Traces for a given list of parents can be pulled using [`client.trace_list()`][watz.Client.trace_list].

```py title="Listing traces"
client.trace_list(["bar@bar.com", "foo@foo.com", "act_2_uid"])
"""
{
    "bar@bar.com": [
        Trace(uid="123", name="measurements", parser_id=2)
    ],
    "foo@foo.com": [],
    "act_2_uid": [
        Trace(uid="678", name="misc", parser_id=2),

        # Further traces will have come from the fit file
        # passed into the activity creation in the previous example.
        ...
    ],
}
"""
```

As a separate step, desired traces can be hydrated with their data using [`client.trace_hydrate()`][watz.Client.trace_hydrate].

Either the full output of a trace_list can be passed, or a specific list of traces. In either case, the output structure is the same as the input, just with [`Trace`][watz.models.Trace] objects replaced with [`TraceWithData`][watz.models.TraceWithData] objects.

!!! info
    [`client.trace_hydrate()`][watz.Client.trace_hydrate] under the hood uses [`client.trace_data()`][watz.Client.trace_data], which is actually returning the raw data.

!!! tip
    These endpoints are separated to minify unwanted data transfer. The request might be rejected if the size of tranfer requested is too large, which is why it can be useful to target exactly what's needed.

```py title="Hydrating traces with data"
traces = client.trace_list(["bar@bar.com", "foo@foo.com", "1_act_uid"])
client.trace_hydrate(traces)
"""
{
    "bar@bar.com": [
        TraceWithData(
            uid="123",
            name="measurements",
            parser_id=2,
            data={"height": 180, "weight": 80},
        )
    ],
    "1_act_uid": [
        TraceWithData(
            uid="789",
            name="activity_misc",
            parser_id=2,
            data=[
                1,
                '2',
                True,
                None,
                ['list'],
                {'dict': 'nested'},
                [4, 5, 6],
                '2021-01-01T00:00:00+00:00',
                {'a': 11, 'b': '12'}
            ],
        )
    ],
}
"""

# Passing a specific list of traces works too, outputting a list to match:
client.traces_hydrate(traces["bar@bar.com"])
"""
[
    TraceWithData(
        uid="123",
        name="measurements",
        parser_id=2,
        data={"height": 180, "weight": 80},
    ),
]
"""
```
