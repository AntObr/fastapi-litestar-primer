import datetime

from litestar import Litestar, asgi, get, post, status_codes, Response, MediaType, Request
from litestar.controller import Controller
from litestar.di import Provide
from litestar.openapi import OpenAPIConfig
from litestar.openapi.datastructures import ResponseSpec
from a2wsgi import WSGIMiddleware

import src.flask_app
from src.downstream import SendingService, PublicSendingException
from src.enums import TimePeriod
from src.fake_db import db
from src.models import Appointment, User


async def get_current_user() -> User:
    """Return the current user."""
    return User(id=1, name="Anthony")

class AppointmentController(Controller):
    path = "/appointment"

    @get(
        path="/list",
        description="Get appointments for a given person over a given time period.",
    )
    async def list_appointments(self, person: str, period: TimePeriod) -> list[Appointment]:
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

    @post(path="/create", status_code=status_codes.HTTP_201_CREATED)
    async def create_appointment(self, data: Appointment) -> str:
        """Submit an appointment."""
        db.append(data)
        return "Appointment created"

@get("/send_private")
async def send_private() -> str:
    SendingService.downstream_service_secret_exception()
    return "Message sent"

@get("/send_public")
async def send_public() -> str:
    SendingService.downstream_service_public_exception()
    return "Message sent"

@get("/current_user", dependencies={"user": Provide(get_current_user)})
async def current_user(user: User) -> str:
    return user.name

def public_sending_exception_handler(request: Request, exc: PublicSendingException) -> Response:
    """Handle `PublicSendingException`."""
    return Response(
        media_type=MediaType.TEXT,
        content=f"validation error: {exc}",
        status_code=status_codes.HTTP_400_BAD_REQUEST,
    )

asgi_flask_app = asgi(path="/", is_mount=True)(
    WSGIMiddleware(src.flask_app.app)
)

app = Litestar(
    route_handlers=[
        AppointmentController,
        send_private,
        send_public,
        current_user,
        asgi_flask_app,
    ],
    exception_handlers={
        PublicSendingException: public_sending_exception_handler,
    },
    debug=True,
    openapi_config=OpenAPIConfig(
        title="Sample Litestar App",
        version="0.0.1",
        use_handler_docstrings=True,
    )
)
