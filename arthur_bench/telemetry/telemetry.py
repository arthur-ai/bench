from amplitude import Amplitude, Identify, BaseEvent
import logging
import uuid
import os

AMPLITUDE_API_KEY = 'bcc009e35e0b79daf089211108eed1de'
amplitude = Amplitude(AMPLITUDE_API_KEY)

TRACK_USAGE_DATA: bool = False

def set_track_usage_data():
    global TRACK_USAGE_DATA
    # If env var BENCH_TELEMTRY_DISABLED is set to anything that is not 0, disable telemetry.
    TRACK_USAGE_DATA = os.getenv('BENCH_TELEMTRY_DISABLED', "0") == "0"

    if TRACK_USAGE_DATA:
        logging.info("Telemetry data is being collected by Arthur! To disable, set the environment variable BENCH_TELEMTRY_DISABLED=1.")


# A no-op if user opts out of data collection.
def send_event(event, user_id):
    if not TRACK_USAGE_DATA:
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
