import datetime
from src.models import Appointment


db = [
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
