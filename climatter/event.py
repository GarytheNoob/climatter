from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class Event:
    the_date: date
    title: str
    tdelta: timedelta = timedelta(0)
    yearly: bool = False
    annivarsary: int = -1

    def checkin(self, today: date | None = None) -> None:
        if today is None:
            today = date.today()
        if self.yearly:
            self.the_date = self.the_date.replace(year=today.year)
            if self.the_date < today:
                self.the_date = self.the_date.replace(
                    year=self.the_date.year + 1
                )
        self.tdelta = self.the_date - today

        if not self.yearly and self.tdelta.days < 0:
            if (
                self.the_date.month == today.month
                and self.the_date.day == today.day
            ):
                self.annivarsary = today.year - self.the_date.year

    def __post_init__(self):
        self.checkin()
