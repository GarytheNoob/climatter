import argparse
import sys

from .display_events import list_events, notify_events
from .event import Event
from .get_events import read_events_from_file


def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Event notifier and lister")
    parser.add_argument("events_file", help="Path to the events file")
    parser.add_argument(
        "-n",
        "--notify",
        action="store_true",
        help="Notify events. If not set, events will be listed instead.",
    )

    parser.add_argument(
        "--dev-today", help="Override today's date (YYYY-MM-DD)"
    )
    return parser.parse_args()


def load_events_with_args(args: argparse.Namespace) -> list[Event]:
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
    args = handle_args()
    events = load_events_with_args(args)
    events.sort(
        key=lambda e: (
            e.tdelta,
            e.title,
        ),
        reverse=True,
    )
    if args.notify:
        notify_events(events)
    else:
        list_events(events)


if __name__ == "__main__":
    main()
