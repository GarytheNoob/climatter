from dataclasses import dataclass
from datetime import timedelta, date

@dataclass
class Event:
    fulldate: str
    date: date
    title: str
    tdelta: timedelta = timedelta(0)
