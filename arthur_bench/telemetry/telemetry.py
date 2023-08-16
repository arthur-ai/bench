# flake8: noqa
from amplitude import Amplitude, BaseEvent
import uuid
import os
from enum import Enum
from arthur_bench.telemetry.config import TelemetryConfig
from arthur_bench.logger.logger import logger


AMPLITUDE_API_KEY = "bcc009e35e0b79daf089211108eed1de"
amplitude = Amplitude(AMPLITUDE_API_KEY)


class Telemetry(Enum):
    ON = 1
    OFF = 2
    LOG = 3


TRACK_USAGE_DATA: Telemetry


def set_track_usage_data(cfg: TelemetryConfig):
    global TRACK_USAGE_DATA
    TRACK_USAGE_DATA = Telemetry.ON if cfg.push_usage_data else Telemetry.OFF

    telemetry = os.getenv("BENCH_TELEMETRY_DISABLED", "0")
    if telemetry == "log":
        TRACK_USAGE_DATA = Telemetry.LOG
    elif telemetry != "0":
        TRACK_USAGE_DATA = Telemetry.OFF

    if TRACK_USAGE_DATA == Telemetry.ON and cfg.log_notice_of_usage_data:
        logger.warn(
            "Anonymous usage data is being collected by Arthur! For more details please see https://github.com/arthur-ai/bench/blob/develop/docs/source/telemetry.md."
        )


# A no-op if user opts out of data collection.
def send_event(event, user_id: uuid.UUID):
    if TRACK_USAGE_DATA == Telemetry.OFF:
        return

    elif TRACK_USAGE_DATA == Telemetry.LOG:
        logger.info(BaseEvent(user_id=str(user_id), **event))
        return

    logger.debug("Pushing usage data to Arthur.")
    amplitude.track(BaseEvent(user_id=str(user_id), **event))

    # Flush the event buffer
    amplitude.flush()
