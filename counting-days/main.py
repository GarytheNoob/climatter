from datetime import datetime, timedelta
from .event import Event

data: list[dict[str, str]] = [
    {"fulldate": "2026-01-01", "event": "New Year's Day"},
    {"fulldate": "2026-02-03", "event": "Special"},
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
            date=datetime.strptime(event["fulldate"], "%Y-%m-%d").date(),
            title=event["event"],
            tdelta=days_wrt_today(event["fulldate"])
        )
        for event in events
    ]

def list_events(events: list[Event]) -> None:
    events.sort(key=lambda e: (e.tdelta 
                                   if e.tdelta.days != 0
                                   else timedelta.min, 
                               e.title))
    for event in events:
        if event.tdelta.days == 0:
            print(f"    Today is {event.title}!")
        else:
            prep = "since" if event.tdelta.days < 0 else "before"
            print(f"{abs(event.tdelta.days):>4} days {prep:<7} {event.title}")

def main() -> None:
    enriched_events = parse_data(data)
    list_events(enriched_events)


if __name__ == "__main__":
    main()
