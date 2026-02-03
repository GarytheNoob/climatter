from dataclasses import dataclass
from datetime import timedelta

@dataclass
class Event:
    fulldate: str
    event: str
    tdelta: timedelta = timedelta(0)
