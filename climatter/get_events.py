from datetime import date
from pathlib import Path

from .event import Event


def read_events_from_file(path_str: str) -> list[Event]:
    file_path = Path(path_str).expanduser()
    events: list[Event] = []
    if (
        # not file_path
        # or not os.path.exists(file_path)
        # or not os.path.isfile(file_path)
        not file_path.is_file()
        or not file_path.exists()
    ):
        print(f"File not found: {path_str}")
        return events
    with file_path.open("r", encoding="utf-8") as file:
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
