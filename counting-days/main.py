from datetime import timedelta

from .display_events import display_events
from .get_events import read_events_from_file


def main() -> None:
    events = read_events_from_file("events/test.events")
    events.sort(
        key=lambda e: (
            e.tdelta if e.tdelta.days != 0 else timedelta.min,
            e.title,
        )
    )
    display_events(events)


if __name__ == "__main__":
    main()
