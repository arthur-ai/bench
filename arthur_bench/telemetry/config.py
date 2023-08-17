import json
import uuid
from pathlib import Path
from pydantic import BaseModel


class TelemetryConfig(BaseModel):
    user_id: str
    log_notice_of_usage_data: bool
    push_usage_data: bool


def _get_config_file_name() -> Path:
    return Path("~/.bench_config/config.json").expanduser()


def get_or_persist_id() -> TelemetryConfig:
    config_file = _get_config_file_name()
    # Create directory if it does not exist.
    config_file.parent.mkdir(exist_ok=True)

    # File exists.  Return its contents.
    if config_file.exists():
        return TelemetryConfig(**json.loads(config_file.open().read()))

    # File doesn't exist.  Generate and return config.
    id = uuid.uuid4()
    new_config = TelemetryConfig(
        user_id=str(id), log_notice_of_usage_data=False, push_usage_data=True
    )
    config_file.open("w+").write(new_config.json())

    # Indicate that file was just created to the caller => we should log notice.
    new_config.log_notice_of_usage_data = True
    return new_config


def persist_usage_data(push_usage_data: bool):
    config_file = _get_config_file_name()
    # Create directory if it does not exist.
    config_file.parent.mkdir(exist_ok=True)

    msg = f"Successfully set Bench anonymous usage data collection to {push_usage_data}"

    if config_file.exists():
        cfg = TelemetryConfig(**json.loads(config_file.open().read()))
        cfg.push_usage_data = push_usage_data
        config_file.open("w+").write(cfg.json())
        print(msg)
        return

    id = uuid.uuid4()
    new_config = TelemetryConfig(
        user_id=str(id), log_notice_of_usage_data=False, push_usage_data=push_usage_data
    )
    config_file.open("w+").write(new_config.json())
    print(msg)
