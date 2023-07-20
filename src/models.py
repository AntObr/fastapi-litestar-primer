import pydantic
import datetime


class User(pydantic.BaseModel):
    """Model for a user."""

    id: int
    name: str


class Appointment(pydantic.BaseModel):
    """Model for an appointment."""

    person: str
    timeslot: datetime.datetime
    notes: str | None = None

    @pydantic.validator("person")
    def validate_person(cls, value: str) -> str:
        if " " not in value:
            raise ValueError("must contain a space")
        return value

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
