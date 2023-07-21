from amplitude import Amplitude, BaseEvent
import logging
import uuid
import os
from enum import Enum


AMPLITUDE_API_KEY = 'bcc009e35e0b79daf089211108eed1de'
amplitude = Amplitude(AMPLITUDE_API_KEY)

class Telemetry(Enum):
    ON = 1
    OFF = 2
    LOG = 3

TRACK_USAGE_DATA: Telemetry = Telemetry.ON

def set_track_usage_data():
    global TRACK_USAGE_DATA

    telemetry = os.getenv('BENCH_TELEMTRY_DISABLED', "0")
    if telemetry == "log":
        TRACK_USAGE_DATA = Telemetry.LOG
    elif telemetry != "0":
        TRACK_USAGE_DATA = Telemetry.OFF

    if TRACK_USAGE_DATA == Telemetry.ON:
        logging.warn("""Telemetry data is being collected by Arthur! To disable, set the environment variable BENCH_TELEMTRY_DISABLED=1.
                     To disable pushing metrics and instead log what would be pushed, set BENCH_TELEMTRY_DISABLED=log.""")


# A no-op if user opts out of data collection.
def send_event(event, user_id: uuid.UUID):
    if TRACK_USAGE_DATA == Telemetry.OFF:
        return

    elif TRACK_USAGE_DATA == Telemetry.LOG:
        logging.info(BaseEvent(user_id=str(user_id),**event))
        return

    logging.info("Pushing usage data to Arthur.")
    amplitude.track(
        BaseEvent(
            user_id=str(user_id),
            **event
        )
    )

    # Flush the event buffer
    amplitude.flush()
