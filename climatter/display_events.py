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
    table = Table.grid(pad_edge=True, padding=(0, 2))

    table.add_column(justify="left", no_wrap=True)
    table.add_column(justify="right", no_wrap=True)
    table.add_column(justify="right", no_wrap=True)

    events = list(filter(lambda e: e.tdelta.days <= 0, events))

    for i, event in enumerate(events):
        # if event.tdelta.days > 0:
        #     continue
        # content = ""
        if event.tdelta.days == 0:
            table.add_row(
                "Today is",
                "",
                f"[i blue b]{event.title}[/i blue b]!",
            )
        elif event.annivarsary > 0:
            table.add_row(
                "Today is",
                f"[bold magenta]{event.annivarsary} years[/bold magenta] since",
                f"[i blue b]{event.title}[/i blue b]!",
            )
        elif abs(event.tdelta.days) % 100 == 0:
            table.add_row(
                "Today is",
                f"[bold cyan]{-event.tdelta.days}  days[/bold cyan] since",
                f"[i blue b]{event.title}[/i blue b]!",
            )
    console.print(table)
