import datetime
import typing

from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, status, Depends


import src.flask_app
from src.models import Appointment, User
from src.enums import TimePeriod
from src.fake_db import db
from src.downstream import PublicSendingException, SendingService


def get_current_user() -> User:
    """Return the current user."""
    return User(id=1, name="Anthony")


app = FastAPI()


@app.exception_handler(PublicSendingException)
async def public_sending_exception_handler(
    request: Request, exc: PublicSendingException
) -> JSONResponse:
    """Handle `PublicSendingException`."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(exc)}
    )


@app.get("/appointments")
async def get_appointments(person: str, period: TimePeriod) -> list[Appointment]:
    """Get appointments for a given person over a given time period."""
    appointments = [
        appointment
        for appointment in db
        if appointment.person.lower() == person.lower()
    ]
    if period == TimePeriod.ALL:
        return appointments
    if period == TimePeriod.PAST:
        return [
            appointment
            for appointment in appointments
            if appointment.timeslot < datetime.datetime.now()
        ]
    if period == TimePeriod.FUTURE:
        return [
            appointment
            for appointment in appointments
            if appointment.timeslot > datetime.datetime.now()
        ]


@app.post("/appointments", status_code=status.HTTP_201_CREATED)
async def post_appointment(appointment: Appointment) -> str:
    """Submit an appointment."""
    db.append(appointment)
    return "Appointment created"


@app.post("/send_private")
async def post_send_private():
    SendingService.downstream_service_secret_exception()
    return "Message sent"


@app.post("/send_public")
async def post_send_public():
    SendingService.downstream_service_public_exception()
    return "Message sent"


CurrentUser = typing.Annotated[User, Depends(get_current_user)]


@app.get("/current_user")
async def current_user(user: CurrentUser) -> str:
    """Use dependencies."""
    return user.name


app.mount("/", WSGIMiddleware(src.flask_app.app))
