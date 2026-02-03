from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class Event:
    # fulldate: str
    date: date
    title: str
    tdelta: timedelta = timedelta(0)
    yearly: bool = False
