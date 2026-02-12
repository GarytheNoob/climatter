from datetime import datetime, timedelta

from .event import Event
from .get_events import read_events_from_file
from .lang.en import *


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
        anniversary = event.annivarsary
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
    list_events(events)


if __name__ == "__main__":
    main()
