import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import yaml

# === Data Classes ===


@dataclass
class Option:
    list_mode: str
    list_future_events_count: int
    list_past_events_count: int


@dataclass
class Config:
    option: Option
    event_lists: dict[str, str]
    dev_today: date | None = None
    notify: bool = False


# === Private Helper Functions ===


def _get_default_config_path() -> Path:
    """Returns the path to the bundled default config file."""
    return Path(__file__).parent / "default_config" / "config.yaml"


def _get_user_config_path() -> Path:
    """Returns the path to the user's config file (may not exist)."""
    return Path.home() / ".config" / "climatter" / "config.yaml"


def _find_config_file(user_path: str | None = None) -> Path:
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
            "falling back..."
        )

    # Priority 2: User config directory
    user_config = _get_user_config_path()
    if user_config.exists():
        return user_config

    # Priority 3: Default bundled config
    return _get_default_config_path()


def _validate_config_data(data: dict[str, Any]) -> None:
    """
    Validates the loaded YAML config structure.
    Raises ValueError with helpful message if validation fails.
    """
    # Check top-level keys
    if "options" not in data:
        raise ValueError("Config missing required 'options' section")

    if "event_lists" not in data:
        raise ValueError("Config missing required 'event_lists' section")

    options = data["options"]

    # Validate list_mode
    if "list_mode" not in options:
        raise ValueError("Config missing 'options.list_mode'")

    valid_modes = {"nearest", "furthest", "all"}
    if options["list_mode"] not in valid_modes:
        raise ValueError(
            f"Invalid list_mode: '{options['list_mode']}'. "
            f"Must be one of: {', '.join(valid_modes)}"
        )

    # event_lists must be a dict
    if not isinstance(data["event_lists"], dict):
        raise ValueError(
            "'event_lists' must be a dictionary mapping names to paths"
        )


# === Public API ===


def read_config(
    config_path: str | None = None, args: argparse.Namespace | None = None
) -> Config:
    """
    Reads and parses the config file.

    Args:
        config_path: Optional path to a specific config file.
                     If None, uses priority: user config → default config

    Returns:
        Config object with parsed configuration

    Raises:
        ValueError: If config validation fails
        yaml.YAMLError: If YAML parsing fails
    """
    # TODO: use args to override config options if provided (e.g. dev_today,
    # notify)

    # Find which config file to use
    config_file = _find_config_file(config_path)

    # Load YAML
    try:
        with config_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise yaml.YAMLError(
            f"Failed to parse config file {config_file}: {e}"
        ) from e

    # Validate structure
    _validate_config_data(data)

    # Extract with defaults for optional fields
    options_data = data["options"]
    option = Option(
        list_mode=options_data["list_mode"],
        list_future_events_count=options_data.get(
            "list_future_events_count", 5
        ),
        list_past_events_count=options_data.get("list_past_events_count", 5),
    )

    # Build Config object
    config = Config(
        option=option,
        event_lists=data["event_lists"],  # Store as-is (strings, unexpanded)
    )

    if args:
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
