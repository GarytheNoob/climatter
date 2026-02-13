from rich.console import Console
from rich.table import Table

from .event import Event


def list_events(events: list[Event]) -> None:
    console = Console()
    table = Table.grid(pad_edge=True, padding=(0, 2))

    # table.add_column()
    table.add_column(no_wrap=True)
    table.add_column(justify="right", min_width=8)
    table.add_column(justify="left")

    for event in events:
        # date_str = event.date.strftime("%Y-%m-%d")
        title = event.title
        tdelta = event.tdelta.days
        noun = "day" if abs(tdelta) == 1 else "days"
        if tdelta > 0:
            table.add_row(
                # date_str,
                f"[italic sky_blue2]{title}",
                f"[bold sky_blue1]{tdelta}",
                f"[sky_blue2]{noun} later",
            )
        elif tdelta < 0:
            table.add_row(
                # date_str,
                f"[italic orange3]{title}",
                f"[bold orange1]{-tdelta}",
                f"[orange3]{noun} ago",
            )
        else:
            table.add_row(
                # date_str,
                f"[yellow i]{title}",
                "[bold yellow]0",
                "[yellow]days",
            )

    console.print(table)


def notify_events(events: list[Event]) -> None:
    console = Console()
    for event in events:
        if event.tdelta.days > 0:
            continue
        if event.tdelta.days == 0:
            console.print(f"Today is [i yellow3]{event.title}[/i yellow3]!")
        elif event.annivarsary > 0:
            # XXX: Only for english, but it's good enough for now
            if 10 <= event.annivarsary % 100 <= 20:
                ordinal = f"{event.annivarsary}th"
            else:
                suffix = {1: "st", 2: "nd", 3: "rd"}.get(
                    event.annivarsary % 10, "th"
                )
                ordinal = f"{event.annivarsary}{suffix}"
            console.print(
                f"Today is the {ordinal} anniversary of [i yellow3]{event.title}[/i yellow3]!"
            )
        elif abs(event.tdelta.days) % 100 == 0:
            console.print(
                f"Today is {abs(event.tdelta.days)} days since [i yellow3]{event.title}[/i yellow3]!"
            )
