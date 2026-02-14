import argparse
import sys

from .config import Config, read_config
from .display_events import filter_events, list_events, notify_events
from .event import Event
from .get_events import read_events_from_file


def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Event notifier and lister")
    # parser.add_argument("events_file", help="Path to the events file")
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


def load_events(config: Config) -> list[Event]:
    events: list[Event] = []
    for event_list in config.event_lists.values():
        e = read_events_from_file(event_list)
        if e:
            events.extend(e)
    if config.dev_today:
        for event in events:
            event.checkin(today=config.dev_today)
    return events


def main():
    args = handle_args()
    config = read_config(args=args)

    events = load_events(config)
    shortlisted_events = filter_events(events, config.option)
    if config.notify:
        notify_events(shortlisted_events)
    else:
        list_events(shortlisted_events)


if __name__ == "__main__":
    main()
