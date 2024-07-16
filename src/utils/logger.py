import sys
import datetime

class Logger:
    """
    A simple logger class that prints log messages to stderr with timestamps.
    Log levels: INFO, DEBUG, WARN, ERROR.
    Can be extended to write logs to a file or integrate with logging frameworks.
    """

    def __init__(self, name: str):
        self.name = name

    def _log(self, level: str, msg: str):
        timestamp = datetime.datetime.now().isoformat()
        print(f"{timestamp} [{self.name}] {level}: {msg}", file=sys.stderr)

    def info(self, msg: str):
        self._log("INFO", msg)

    def debug(self, msg: str):
        self._log("DEBUG", msg)

    def warn(self, msg: str):
        self._log("WARN", msg)

    def error(self, msg: str):
        self._log("ERROR", msg)

    # Potential future improvements:
    # - Add a verbosity level
    # - Write to log files
    # - Integrate Python's `logging` module
