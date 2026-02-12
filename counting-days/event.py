from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class Event:
    date: date
    title: str
    tdelta: timedelta = timedelta(0)
    yearly: bool = False
    annivarsary: int = -1

    def __post_init__(self):
        today = date.today()
        if self.yearly:
            self.date = self.date.replace(year=today.year)
            if self.date < today:
                self.date = self.date.replace(year=self.date.year + 1)
        self.tdelta = self.date - today

        if not self.yearly and self.tdelta.days < 0:
            if self.date.month == today.month and self.date.day == today.day:
                self.annivarsary = today.year - self.date.year
