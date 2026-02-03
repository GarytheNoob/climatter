from datetime import datetime, timedelta
from .event import Event

data: list[dict[str, str]] = [
    {"fulldate": "2026-01-01", "event": "New Year's Day"},
    {"fulldate": "2026-02-03", "event": "Today! Special"},
    {"fulldate": "2026-07-04", "event": "Independence Day"},
    {"fulldate": "2026-12-25", "event": "Christmas Day"},
]


def parse_data(events: list[dict[str, str]]) -> list[Event]:

    def days_wrt_today(target_date_str: str) -> timedelta:
        today = datetime.today().date()
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
        return target_date - today

    return [
        Event(
            fulldate=event["fulldate"],
            event=event["event"],
            tdelta=days_wrt_today(event["fulldate"])
        )
        for event in events
    ]

def main() -> None:
    enriched_events = parse_data(data)
    for event in enriched_events:
        print(f"Event: {event.event}, Date: {event.fulldate}, Days until: {event.tdelta.days}")


if __name__ == "__main__":
    main()
