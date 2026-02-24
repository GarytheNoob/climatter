# cliMatter - Remember what matters, in terminal

**cliMatter** is a [DaysMatter](https://app.ipad.ly/idays)-like terminal application
that helps you remember important dates and events.

## Features (Under development)

- [x] Read events from a local list file.

- [x] List all your important dates and events, with the number of days until or
      since each event.

- [x] Notify if today is an important day (event, annivarsary of past event,
      hundred-day since past event, etc).

- [x] Configure
  - [x] Support multiple list files for different categories of events.

  - [x] Configurable number of lines displayed when listing.

  - [x] Load local configuration from file.

- [ ] Tags: Support tagging events for better organization and filtering.
  - [ ] Allow users to filter events by tags when listing.

  - [ ] Custom color coding for different tags.

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
usage: climatter [-h] [--config CONFIG] [-n] [--dev-today DEV_TODAY]

Event notifier and lister

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to config file. If not set, uses priority:
                        user config → default config
  -n, --notify          Notify events. If not set, events will be listed
                        instead.
  --dev-today DEV_TODAY
                        Override today's date (YYYY-MM-DD)
```

### Configuration

cliMatter can be configured using a local configuration file. By default, it
looks for a user configuration file at `~/.config/climatter/config.yaml`. You
can also specify a custom configuration file using the `--config` option.

The default configuration file is located at `./climatter/default_config/config.yaml`
in the project directory. You can copy this file to your user configuration path
and modify it as needed.

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
