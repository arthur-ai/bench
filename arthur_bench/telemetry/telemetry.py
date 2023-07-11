from amplitude import Amplitude, Identify, BaseEvent
import logging
import uuid

AMPLITUDE_API_KEY = 'bcc009e35e0b79daf089211108eed1de'
amplitude = Amplitude(AMPLITUDE_API_KEY)

TRACK_USAGE_DATA: bool = False
USER_ID: uuid.UUID


def set_track_usage_data(id: uuid.UUID, set_usage_data: bool = False):
    global TRACK_USAGE_DATA
    if set_usage_data:
        TRACK_USAGE_DATA = True
        logging.info("Pushing bench usage data to Arthur.")
    global USER_ID
    USER_ID = id


# A no-op if user opts out of data collection.
def send_event(event):
    if not TRACK_USAGE_DATA:
        return

    logging.info("Pushing usage data to Arthur.")
    amplitude.track(
        BaseEvent(
            user_id=str(USER_ID),
            **event
        )
    )

    # Flush the event buffer
    amplitude.flush()
