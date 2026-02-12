from rich import box
from rich.console import Console
from rich.table import Table

from .event import Event


def display_events(events: list[Event]) -> None:
    console = Console()
    table = Table(box=box.SIMPLE_HEAD)

    table.add_column("Date", style="white")
    table.add_column("Title", style="cyan", no_wrap=True)
    table.add_column(style="magenta", justify="right")

    for event in events:
        date_str = event.date.strftime("%Y-%m-%d")
        title = event.title
        tdelta = event.tdelta.days
        table.add_row(date_str, title, str(tdelta))

    console.print(table)
