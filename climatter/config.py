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


def _read_yaml_config(config_file: Path) -> dict[str, Any]:
    try:
        with config_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data is None:
            raise ValueError(f"Config file {config_file} is empty or invalid")
        if not isinstance(data, dict):
            raise ValueError(
                f"Config file {config_file} must contain a YAML dictionary at the top level"
            )
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file not found: {config_file}") from e
    except yaml.YAMLError as e:
        raise yaml.YAMLError(
            f"Failed to parse config file {config_file}: {e}"
        ) from e
    except Exception as e:
        raise Exception(f"Error reading config file {config_file}: {e}") from e
    return data


def _get_default_config() -> dict[str, Any]:
    return {
        "option": {
            "list_mode": "nearest",
            "list_future_events_count": 5,
            "list_past_events_count": 5,
        },
        "event_lists": {
            "default": "~/.config/climatter/events",
        },
    }


def _get_user_config() -> dict[str, Any]:
    user_config_path = Path("~/.config/climatter/config.yaml").expanduser()
    if user_config_path.exists() and user_config_path.is_file():
        return _read_yaml_config(user_config_path)
    return {}


def _merge_configs(
    default: dict[str, Any], user: dict[str, Any]
) -> dict[str, Any]:
    merged = default.copy()
    for key, value in user.items():
        if (
            key == "option"
            and isinstance(value, dict)
            and key in merged
            and isinstance(merged[key], dict)
        ):
            merged[key] = _merge_configs(merged[key], value)
        else:
            merged[key] = value
    return merged


# === Public API ===


def load_config(args: argparse.Namespace) -> Config:
    default_config = _get_default_config()
    user_config = _get_user_config()
    merged_config = _merge_configs(default_config, user_config)

    if args.config:  # runtime config file has highest priority
        runtime_config = _read_yaml_config(Path(args.config).expanduser())
        merged_config = _merge_configs(merged_config, runtime_config)

    if args.mode:
        merged_config["option"]["list_mode"] = args.mode

    option_data = merged_config.get("option", {})
    event_lists_data = merged_config.get("event_lists", {})

    option = Option(
        list_mode=option_data.get("list_mode", "nearest"),
        list_future_events_count=option_data.get("list_future_events_count", 5),
        list_past_events_count=option_data.get("list_past_events_count", 5),
    )

    if args.dev_today:
        try:
            dev_today = date.fromisoformat(args.dev_today)
        except ValueError as e:
            raise ValueError(
                f"Invalid date format for --dev-today: {args.dev_today}. Expected YYYY-MM-DD."
            ) from e
    else:
        dev_today = None

    return Config(
        option=option,
        event_lists=event_lists_data,
        dev_today=dev_today,
        notify=args.notify,
    )
