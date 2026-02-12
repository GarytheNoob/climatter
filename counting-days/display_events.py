from rich.console import Console
from rich.table import Table

from .event import Event


def display_events(events: list[Event]) -> None:
    console = Console()
    table = Table.grid(pad_edge=True, padding=(0, 2))

    # table.add_column()
    table.add_column(no_wrap=True)
    table.add_column(justify="right")
    table.add_column(justify="left")

    for event in events:
        # date_str = event.date.strftime("%Y-%m-%d")
        title = event.title
        tdelta = event.tdelta.days
        if tdelta > 0:
            table.add_row(
                # date_str,
                f"[sky_blue2]{title}",
                f"[bold sky_blue1]{tdelta} [bold sky_blue2]days",
                "[bold sky_blue2]left",
            )
        elif tdelta < 0:
            table.add_row(
                # date_str,
                f"[orange3]{title}",
                f"[bold orange1]{-tdelta} [bold orange3]days",
                "[orange3]ago",
            )
        else:
            table.add_row(
                # date_str,
                f"[yellow]{title}",
                "[bold yellow]TODAY",
                "",
            )

    console.print(table)
