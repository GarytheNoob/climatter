# cliMatter - Remember what matters, in terminal

**cliMatter** is a [DaysMatter](https://app.ipad.ly/idays)-like terminal application
that helps you remember important dates and events.

## Features (Under development)

- [x] Read events from a local list file.

- [x] List all your important dates and events, with the number of days until or
      since each event.

- [x] Notify if today is an important day (event, annivarsary of past event,
      hundred-day since past event, etc).

- [ ] Tags: Support tagging events for better organization and filtering.
  - [ ] Allow users to filter events by tags when listing.

  - [ ] Custom color coding for different tags.

- [ ] Configure
  - [ ] Support multiple list files for different categories of events.

  - [ ] Configurable number of lines displayed when listing.

  - [ ] Load local configuration from file.

## Installation

1. Clone the repository

   ```bash
   git clone https://github.com/GarytheNoob/climatter.git
   ```

1. Navigate to the project directory

   ```bash
   cd climatter
   ```

1. Install cliMatter using [pipx](https://pipx.pypa.io)

   ```bash
   pipx install .
   ```

## Usage

After installation, you can use the `climatter` command in your terminal.

Run `climatter --help` to see available commands and options:

> [!WARNING]
> The following usage information is based on the current development version
> and may change in the future. Update of this README may lag behind the actual
> implementation. Please refer to the command-line help for the most up-to-date
> usage information.

```text
usage: climatter [-h] [-n] [--dev-today DEV_TODAY] events_file

Event notifier and lister

positional arguments:
  events_file           Path to the events file

options:
  -h, --help            show this help message and exit
  -n, --notify          Notify events. If not set, events will be listed
                        instead.
  --dev-today DEV_TODAY
                        Override today's date (YYYY-MM-DD)
```

### Event List File

You need to create a local event list file in the following format:

```
# Comments take whole lines and begin with '#'
# Each line represents an event in the format:
# For a one-time event:
# YYYY-MM-DD;;Event Title
# For a recurring annual event:
# MM-DD;;Event Title
# Example:

01-01;;New Year's Day
12-25;;Christmas
1990-07-15;;John's Birthday
```

Save this file and provide its path to `climatter`.
