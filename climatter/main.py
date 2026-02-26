import argparse

from .config import read_config
from .display_events import filter_events, list_events, notify_events
from .get_events import load_events


def handle_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Event notifier and lister")
    parser.add_argument(
        "--config",
        help="Path to config file. If not set, uses priority: user config → default config",
    )
    parser.add_argument(
        "-n",
        "--notify",
        action="store_true",
        help="Notify events. If not set, events will be listed instead.",
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=["nearest", "furthest", "all"],
        help="List mode: 'nearest' (default), 'furthest', or 'all'",
    )
    parser.add_argument(
        "--dev-today", help="Override today's date (YYYY-MM-DD)"
    )
    return parser.parse_args()


def main():
    args = handle_args()
    config = read_config(args)

    events = load_events(config)
    if config.notify:
        notify_events(events)
    else:
        shortlisted_events = filter_events(events, config.option)
        list_events(shortlisted_events)


if __name__ == "__main__":
    main()
