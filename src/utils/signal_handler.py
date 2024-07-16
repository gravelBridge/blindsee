import signal
import sys
from .logger import Logger

class GracefulKiller:
    """
    GracefulKiller sets up signal handlers for SIGINT and SIGTERM,
    allowing the program to shut down gracefully.
    When triggered, sets kill_now to True so that the main loop can end safely.
    """

    def __init__(self):
        self.logger = Logger("SignalHandler")
        self.kill_now = False
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.logger.info(f"Received termination signal ({signum}). Exiting gracefully...")
        self.kill_now = True

    # Future ideas:
    # - Add cleanup callbacks
    # - Integrate with other system components for graceful resource release
