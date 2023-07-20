import enum


class TimePeriod(enum.StrEnum):
    """A period of time."""

    ALL = "all"
    PAST = "past"
    FUTURE = "future"
