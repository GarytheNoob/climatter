from datetime import datetime, timedelta
from typing import Any

from .event import Event
from .get_events import read_events_from_file
from .lang.en import *


def normalize_events(events: list[Event]) -> list[Event]:
    for event in events:
        if event.yearly:
            event_date = event.date.replace(year=datetime.now().year)
            if event_date < datetime.now().date():
                event_date = event_date.replace(year=event_date.year + 1)
            event.tdelta = event_date - datetime.now().date()
        else:
            event.tdelta = event.date - datetime.now().date()
    return events


def check_anniversary_since(event: Event) -> int:
    if event.tdelta.days >= 0 or event.yearly:
        return -1
    if (
        event.date.month == datetime.now().month
        and event.date.day == datetime.now().day
    ):
        years = datetime.now().year - event.date.year
        return years
    return -1


def list_events(events: list[Event]) -> None:
    events.sort(
        key=lambda e: (
            e.tdelta if e.tdelta.days != 0 else timedelta.min,
            e.title,
        )
    )
    for event in events:
        if event.tdelta.days == 0:
            print(f"{TODAY_STR}: {event.title}")
            continue
        anniversary = check_anniversary_since(event)
        is_hundreds_days = not event.tdelta.days % 100 and event.tdelta.days < 0
        if anniversary > 0:
            print(ANNIVERSARY_STR.format(anniv=anniversary, title=event.title))
        elif is_hundreds_days:
            print(
                HUNDREDS_DAY_STR.format(
                    days=abs(event.tdelta.days), title=event.title
                )
            )
        else:
            print(
                (
                    DAYS_BEFORE_STR if event.tdelta.days > 0 else DAYS_AFTER_STR
                ).format(title=event.title, days=abs(event.tdelta.days))
            )


def main() -> None:
    events = read_events_from_file("events/test.events")
    enriched_events = normalize_events(events)
    list_events(enriched_events)


if __name__ == "__main__":
    main()
