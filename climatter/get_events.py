import os
from datetime import date

from .event import Event


def read_events_from_file(file_path: str) -> list[Event]:
    file_path = os.path.abspath(os.path.expanduser(file_path))
    events: list[Event] = []
    if (
        not file_path
        or not os.path.exists(file_path)
        or not os.path.isfile(file_path)
    ):
        print(f"File not found: {file_path}")
        return events
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                if not line.strip() or line.strip().startswith("#"):
                    continue
                date_str, title = line.strip().split(";;", 2)
                date_parts = date_str.split("-")
                if len(date_parts) == 3:
                    year, month, day = map(int, date_parts)
                    event = Event(the_date=date(year, month, day), title=title)
                elif len(date_parts) == 2:
                    month, day = map(int, date_parts)
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
