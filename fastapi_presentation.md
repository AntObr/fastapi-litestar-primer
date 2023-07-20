---
marp: true
theme: uncover
---

# FastAPI Primer

![bg fit right](tweet.jpg)

---

# FastAPI

> [...] a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.  

---

**Technologies!**

**Uvicorn**
An ASGI web server implementation for Python.

**Starlette**
a lightweight ASGI framework/toolkit, which is ideal for building async web services in Python.

**Pydantic**
Data validation and settings management using Python type annotations.

**FastAPI**

---

**Models!**

```python
class Appointment(pydantic.BaseModel):
    """Model for an appointment."""

    person: str
    timeslot: datetime.datetime
    notes: str | None
```

```python
class TimePeriod(enum.StrEnum):
    """A period of time."""

    ALL = "all"
    PAST = "past"
    FUTURE = "future"
```

---

**Database!**

```python
fake_db = [
    Appointment(
        person="Anthony A",
        timeslot=datetime.datetime(2023, 7, 12, 11, 0, 0),
        notes="Here are some notes about the appointment.",
    ),
    Appointment(
        person="Anthony A",
        timeslot=datetime.datetime(2023, 7, 20, 12, 0, 0),
    ),
    Appointment(
        person="Anthony A",
        timeslot=datetime.datetime(2023, 5, 20, 13, 0, 0),
        notes="This is an old appointment.",
    ),
    Appointment(
        person="Barry B",
        timeslot=datetime.datetime(2023, 7, 20, 12, 0, 0),
    ),
    Appointment(
        person="Timothy T",
        timeslot=datetime.datetime(2023, 7, 20, 12, 0, 0),
    ),
]
```

---

**A Basic App**

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/appointments")
async def get_appointments(person: str, period: TimePeriod) -> list[Appointment]:
    """Get appointments for a given person over a given time period."""
    ...
```

```sh
$ uvicorn main:app --reload
```

<!-- Demonstrate openapi spec -->

---

**Basic Data Validation!**

```sh
curl -X 'GET' \
  'http://127.0.0.1:8000/appointments?person=Anthony%20A&period=invalid' \
  -H 'accept: application/json'
```

```sh
{
    "detail": [
        {
            "loc": ["query","period"],
            "msg": "value is not a valid enumeration member; permitted: 'all', 'past', 'future'",
            "type": "type_error.enum",
            "ctx":{
                "enum_values": ["all","past","future"]
            }
        }
    ]
}
```

---

**Custom Data Validation!**

```python
class Appointment(pydantic.BaseModel):
    """Model for an appointment."""
    ...

    @pydantic.validator("person")
    def validate_person(cls, value: str) -> str:
        if " " not in value:
            raise ValueError("must contain a space")
        return value
```

```python
@app.post("/appointments", status_code=status.HTTP_201_CREATED)
async def post_appointment(appointment: Appointment) -> str:
    """Submit an appointment."""
    fake_db.append(appointment)
    return "Appointment created"
```

<!-- Demonstrate validation -->

---

**Hidden Exceptions!**

```python
class SecretSendingException(Exception):
    """An exception we don't want clients to see."""

class SendingService:

    @staticmethod
    def downstream_service_secret_exception():
        raise SecretSendingException("API Key invalid")
```

```python
@app.post("/send_private")
async def post_send_private():
    SendingService.downstream_service_secret_exception()
    return "Message sent"
```


<!-- By default FastAPI transforms uncaught exceptions into a generic 500 response -->

---

**Public Exceptions!**

```python
class PublicSendingException(Exception):
    """An exception we want to pass on to clients."""

class SendingService:

    @staticmethod
    def downstream_service_public_exception():
        raise PublicSendingException("Message too long")
```

```python
@app.post("/send_public")
async def post_send_public():
    SendingService.downstream_service_public_exception()
    return "Message sent"
```

---

**Exception Handlers!**

```python
@app.exception_handler(PublicSendingException)
async def public_sending_exception_handler(
    request: Request,
    exc: PublicSendingException
) -> JSONResponse:
    """Handle `PublicSendingException`."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)}
    )
```

---

**Dependencies!**

```python
class User(pydantic.BaseModel):
    """Model for a user."""
    id: int
    name: str
```

```python
def get_current_user() -> User:
    """Return the current user."""
    return User(id=1, name ="Anthony")
```

```python
CurrentUser = typing.Annotated[User, Depends(get_current_user)]

@app.get("/current_user")
async def current_user(user: CurrentUser) -> str:
    """Use dependencies."""
    return user.name
```

---

**More Documentation!**

```python
class Appointment(pydantic.BaseModel):
    """Model for an appointment."""
    ...

    class Config:
        fields = {
            "person": {
                "description": "The name of the person who the appointment is for.",
            },
            "timeslot": {
                "description": "A datetime representation of the timeslot start.",
            },
            "notes": {
                "description": "Optional notes associated with the appointment.",
            },
        }

        schema_extra = {
            "example": {
                "person": "Anthony A",
                "timeslot": "2023-06-29T10:07:53.487Z",
                "notes": "Child seat required",
            }
        }
```

---

**Migrating from Flask!**

```python
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, request

flask_app = Flask(__name__)

@flask_app.route("/hello_flask")
def hello_flask() -> str:
    """A flask route."""
    name = request.args.get("name", "World!")
    return f"Hello, {name} from Flask!"

app.mount("/", WSGIMiddleware(flask_app))
```

---

**More Migration!**

**forethought.ai**
Migrated from Flask to FastAPI and provided some great blog posts about the process

**Disclaimer:** The creator of FastAPI works for Forethought and wrote those blog posts

<!-- https://engineering.forethought.ai/blog/2022/12/01/migrating-from-flask-to-fastapi-part-1/ -->
<!-- https://engineering.forethought.ai/blog/2023/02/14/migrating-from-flask-to-fastapi-part-2/ -->
<!-- https://engineering.forethought.ai/blog/2023/02/28/migrating-from-flask-to-fastapi-part-3/ -->
