import argparse
import sys

from .display_events import list_events, notify_events
from .event import Event
from .get_events import read_events_from_file


def load_events_with_args() -> list[Event]:
    parser = argparse.ArgumentParser(description="Event notifier and lister")
    parser.add_argument("events_file", help="Path to the events file")
    parser.add_argument(
        "--dev-today", type=str, help="Override today's date (YYYY-MM-DD)"
    )
    args = parser.parse_args()
    loaded_events = read_events_from_file(args.events_file)
    if args.dev_today:
        from datetime import datetime

        try:
            dev_today = datetime.fromisoformat(args.dev_today).date()
        except ValueError:
            print(
                f"Invalid date format for --dev-today: {args.dev_today}\n"
                "Expected format: YYYY-MM-DD"
            )
            sys.exit(1)
        for e in loaded_events:
            e.checkin(today=dev_today)
    return loaded_events


def main():
    events = load_events_with_args()
    events.sort(
        key=lambda e: (
            e.tdelta,
            e.title,
        ),
        reverse=True,
    )
    notify_events(events)
    list_events(events)


if __name__ == "__main__":
    main()
