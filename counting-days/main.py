from datetime import datetime

events: list[dict[str, str]] = [
    {"fulldate": "2026-01-01", "event": "New Year's Day"},
    {"fulldate": "2026-02-03", "event": "Today! Special"},
    {"fulldate": "2026-07-04", "event": "Independence Day"},
    {"fulldate": "2026-12-25", "event": "Christmas Day"},
]

def main() -> None:
    today = datetime.today().date()
    today_event = next(
        (event for event in events
            if event["fulldate"] == today.strftime("%Y-%m-%d")),
        None)
    if today_event:
        print(f"Today is {today_event['event']}!")

    upcoming_events = [
        event for event in events if datetime.strptime(event["fulldate"], "%Y-%m-%d").date() >= today
    ]
    upcoming_events.sort(key=lambda x: x["fulldate"])

    if upcoming_events:
        next_event = upcoming_events[0]
        print(f"The next event is {next_event['event']} on {next_event["fulldate"]}.")
    else:
        print("There are no upcoming events.")


if __name__ == "__main__":
    main()
