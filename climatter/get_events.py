from datetime import date
from pathlib import Path

from .config import Config
from .event import Event


def _validate_month_day(month: int, day: int) -> bool:
    if month < 1 or month > 12:
        return False
    if day < 1:
        return False
    if month in {1, 3, 5, 7, 8, 10, 12} and day > 31:
        return False
    if month in {4, 6, 9, 11} and day > 30:
        return False
    if month == 2 and day > 29:
        return False
    return True


def read_events_from_file(path_str: str) -> list[Event]:
    file_path = Path(path_str).expanduser()
    events: list[Event] = []
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return events
    if not file_path.is_file():
        print(f"Invalid file path (not a file): {file_path}")
        return events
    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            try:
                if not line.strip() or line.strip().startswith("#"):
                    continue

                date_str, title = line.strip().split(";;", 1)
                date_parts = date_str.split("-")
                if len(date_parts) == 3:
                    year, month, day = map(int, date_parts)

                    if not _validate_month_day(month, day):
                        raise ValueError(
                            f"Invalid date: {date_str} in line: {line.strip()}"
                        )

                    event = Event(the_date=date(year, month, day), title=title)

                elif len(date_parts) == 2:
                    month, day = map(int, date_parts)

                    if not _validate_month_day(month, day):
                        raise ValueError(
                            f"Invalid date: {date_str} in line: {line.strip()}"
                        )

                    event = Event(
                        the_date=date(1, month, day), title=title, yearly=True
                    )

                else:
                    raise ValueError("Invalid date format")

            except ValueError:
                print(f"Invalid line format: {line.strip()}")
                continue
            else:
                events.append(event)
    return events


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
