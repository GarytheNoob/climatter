import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml

# === Data Classes ===


@dataclass
class Option:
    list_mode: str = "nearest"
    list_future_events_count: int = 5
    list_past_events_count: int = 5


@dataclass
class Config:
    option: Option
    event_lists: dict[str, str]
    dev_today: date | None = None
    notify: bool = False


# === Private Helper Functions ===


def _get_user_config_path() -> Path:
    """Returns the path to the user's config file (may not exist)."""
    return Path.home() / ".config" / "climatter" / "config.yaml"


def _find_config_file(user_path: str | None = None) -> Path | None:
    """
    Finds the config file to use based on priority:
    1. User-specified path (if provided and exists)
    2. User config at ~/.config/climatter/config.yaml (if exists)
    3. Default bundled config (always exists)

    Returns: Path object to the config file to use
    """
    # Priority 1: User-specified path
    if user_path:
        user_provided = Path(user_path).expanduser()
        if user_provided.exists():
            return user_provided
        # Fall through to next priority with warning
        print(
            f"Warning: Specified config file not found: {user_path}, "
            + "falling back..."
        )

    # Priority 2: User config directory
    user_config = _get_user_config_path()
    if user_config.exists():
        return user_config

    # Priority 3: Default bundled config
    return None


# === Public API ===


def read_config(args: argparse.Namespace | None = None) -> Config:
    """
    Reads and parses the config file.

    Args:
        args: Optional argparse.Namespace containing command-line options.
            Relevant attributes include:
            - config: Optional path to a specific config file. If not set,
              the default search priority is applied (user config → default
              config).
            - dev_today: Optional override for today's date in ISO format
              (YYYY-MM-DD), used for development/testing.
            - notify: Optional notification flag/setting applied to the
              returned Config object.
            - mode: Optional list mode override applied to the returned Config
              object.
    Returns:
        Config object with parsed configuration

    Raises:
        ValueError: If config validation fails
        yaml.YAMLError: If YAML parsing fails
    """

    # Find which config file to use
    config_file = _find_config_file(args.config if args else None)

    config = Config(
        option=Option(),  # Defaults
        event_lists={
            "default": "~/.config/climatter/events",
        },
    )

    if config_file:
        # Load YAML
        try:
            with config_file.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(
                f"Failed to parse config file {config_file}: {e}"
            ) from e
        if data is None:
            raise ValueError(f"Config file {config_file} is empty or invalid")
        if not isinstance(data, dict):
            raise ValueError(
                f"Config file {config_file} must contain a YAML dictionary at the top level"
            )

        # Extract with defaults for optional fields
        if "options" in data and isinstance(data["options"], dict):
            options_data = data["options"]
            if "list_mode" in options_data:
                config.option.list_mode = options_data["list_mode"]
            if "list_future_events_count" in options_data:
                config.option.list_future_events_count = options_data[
                    "list_future_events_count"
                ]
            if "list_past_events_count" in options_data:
                config.option.list_past_events_count = options_data[
                    "list_past_events_count"
                ]

        # Build Config object
        if "event_lists" in data and isinstance(data["event_lists"], dict):
            config.event_lists = data["event_lists"]

    if args:
        if args.mode:
            config.option.list_mode = args.mode
        if args.dev_today:
            from datetime import datetime

            try:
                config.dev_today = datetime.fromisoformat(args.dev_today).date()
            except ValueError as e:
                raise ValueError(
                    f"Invalid date format for --dev-today: {args.dev_today}.\n"
                    + "Expected format: YYYY-MM-DD"
                ) from e

        config.notify = args.notify

    return config
