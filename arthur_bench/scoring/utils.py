import logging


class suppress_warnings:
    """
    A context-manager class to temporarily set the logging level for a logger to ERROR
    before returning it to its previous state.
    """

    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)
        self.original_state = (
            self.logger.level
        )  # note: we get actual level not effective level, could be UNSET

    def __enter__(self):
        self.logger.setLevel(logging.ERROR)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.setLevel(
            self.original_state
        )  # it's ok to use setLevel() to set to anything, even NOTSET
