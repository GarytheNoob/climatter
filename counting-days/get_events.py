from datetime import date

from .event import Event


def read_events(file_path: str) -> list[Event]:
    events = []
    with open(file_path, "r") as file:
        for line in file:
            try:
                date_str, title = line.strip().split(";;", 2)
                date_parts = date_str.split("-")
                if len(date_parts) == 3:
                    year, month, day = map(int, date_parts)
                    event = Event(date=date(year, month, day), title=title)
                elif len(date_parts) == 2:
                    month, day = map(int, date_parts)
                    event = Event(
                        date=date(1, month, day), title=title, yearly=True
                    )
                else:
                    raise ValueError("Invalid date format")
                events.append(event)
            except ValueError:
                print(f"Invalid line format: {line.strip()}")
                continue
    return events
