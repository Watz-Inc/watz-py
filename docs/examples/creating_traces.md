The input of data into the system is only restricted to the types on the [Conversions Page](conversions.md), how the data is structured is left mostly up to the user.

Data relating to individuals and activities is often temporal, and falls into some standard patterns outlined below.

## Initialization

Let's create a client, subject and activity to work with:

```py title="Initialization"
import watz

client = watz.Client(secret="my api key")

client.subject_create([
    watz.models.NewSubject(email="foo@bar.com"),
])

activities = client.activity_create([
    watz.models.NewActivity(subject_uid="foo@bar.com")
])

act_uid = activities[0].uid
```

## Static Data

Some data is static, meaning it is not recorded over time.

Examples include:

- A subject's date of birth
- A subject's height
- Calories burnt during an activitiy
- Information about sensors recording during an activity

The data can be structured arbitrarily, some examples are shown below:

```py title="Static Data"
import datetime as dt

client.trace_create([

    # <-- Subject traces
    
    watz.models.NewTrace(
        parent_uid="foo@bar.com",
        name="profile",
        data={
            "name": "foo bar",
            "dob": dt.date(1990, 1, 1),
            "height": {
                "value": 180,
                "unit": "cm",
            },
            "gender": "m",
        },
    ),

    # <-- Activity traces

    watz.models.NewTrace(
        parent_uid=act_uid,
        name="calories",
        data=678,
    ),
    watz.models.NewTrace(
        parent_uid=act_uid,
        name="sensors",
        data=[
        {
            "name": "accelerometer",
            "id": "123",
        }, 
        {
            "name": "gyroscope",
            "id": "456",
        }],
    ),
])
```

## Temporal Data
A lot of data is temporal, meaning it is recorded over time, where each recording is associated with a timestamp.

Examples include:

- A subject's weight
- A subject's resting heart rate
- Heart rate or power output during an activity
- GPS coordinates during an activity

The data can be structured arbitrarily, some examples are shown below:

```py title="Temporal Data"
import datetime as dt

client.trace_create([

    # <-- Subject traces

    watz.models.NewTrace(
        parent_uid="foo@bar.com",
        name="weight",
        data={
            "unit": "kg",
            "values": [
                (65.3, dt.datetime(2021, 1, 1)), 
                (65.2, dt.datetime(2021, 1, 2)), 
            ],
        },
    ),
    watz.models.NewTrace(
        parent_uid="foo@bar.com",
        name="resting_heart_rate",
        data={
            "unit": "bpm",
            "values": [65, 64],
            "timestamps": [
                dt.datetime(2021, 1, 1), 
                dt.datetime(2021, 1, 2), 
            ],
        },
    ),    

    # <-- Activity traces

    # If attributes share a temporal trace, they could be stored together:
    watz.models.NewTrace(
        parent_uid=act_uid,
        name="hr/power",
        data={
            "hr": {
                "unit": "bpm",
                "values": [102, 110]
            },
            "power": {
                "unit": "watts", 
                "values": [200, 210],
            },
            "timestamps": [
                dt.datetime(2021, 1, 1), 
                dt.datetime(2021, 1, 2), 
            ],
        },
    ),

    # Alternatively, traces could reference a shared temporal trace:
    watz.models.NewTrace(
        parent_uid=act_uid,
        name="coord_ts",
        data=[
            dt.datetime(2021, 1, 1), 
            dt.datetime(2021, 1, 2), 
        ]
    ),
    watz.models.NewTrace(
        parent_uid=act_uid,
        name="lat",
        data={
            "values": [1.234, 1.235],
            "ts_trace_name": "coord_ts",
        },
    ),
    watz.models.NewTrace(
        parent_uid=act_uid,
        name="long",
        data={
            "values": [1.234, 1.235],
            "ts_trace_name": "coord_ts",
        },
    ),    
])
```
!!! note
    `datetime.datetime` is used here for simplicity, using pre-serialized timestamps would make no difference.

!!! note
    Support for updating & deleting existing traces coming soon.
