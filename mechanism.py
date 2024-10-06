# Built-in libraries
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
import threading
from time import sleep
import sys
from typing import Optional, Callable


logger = logging.getLogger(__name__)


class Quartz(threading.Thread):
    """
    A thread that periodically updates the screen with a timestamp, similar to
    a clock mechanism.

    This thread fetches the current timestamp every second, optionally using a specified timezone,
    and invokes the provided `update` method to refresh the screen until stopped.
    """

    def __init__(
        self, update: Callable[[int], None], tz: Optional[ZoneInfo] = None
    ) -> None:
        """
        Initialize the Quartz thread.

        Args:
            update (Callable[[int], None]): Function to call with the Unix timestamp to update the screen.
            tz (Optional[ZoneInfo]): Timezone to use for timestamps. Defaults to the local timezone.
        """
        super().__init__(name="QuartzClock", daemon=True)
        self.update = update
        self.tz_info = tz
        self.__stop_event = threading.Event()
        self.start()

    def run(self) -> None:
        """
        Main loop of the Quartz thread.

        Continuously fetches the current system timestamp, respects the provided timezone (or defaults to
        the system's local timezone), and calls the `update` function with it every second until stopped.
        """
        try:

            while not self.__stop_event.wait(timeout=1):

                now = datetime.now(tz=self.tz_info)
                timestamp = int(now.timestamp())
                self.update(timestamp)

            logger.info("Screen update thread stopped.")

        except threading.ThreadError as e:
            logging.error(f"An error occurred during the thread operation: {e}")
            sys.exit(1)  # Exit the program in case of an error

    def stop(self) -> None:
        """Stops the Quartz thread by setting the stop event."""
        self.__stop_event.set()