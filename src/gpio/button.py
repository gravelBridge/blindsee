import RPi.GPIO as GPIO
import time
from ..utils.logger import Logger
from ..config.config import Config
from typing import Callable, Optional

class Button:
    """
    Manages a physical button connected to a GPIO pin.
    Uses an internal pull-up and detects falling edges.
    Debouncing is handled via GPIO event detection and software timing.
    When pressed, triggers a callback.
    """

    def __init__(self):
        self.logger = Logger("Button")
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(Config.BUTTON_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.logger.info(f"Button set up on GPIO pin {Config.BUTTON_GPIO_PIN} with internal pull-up.")
        except RuntimeError as e:
            self.logger.error(f"Error setting up GPIO: {e}. Make sure you run as root or in a correct environment.")
        except Exception as ex:
            self.logger.error(f"Unexpected error in button setup: {ex}")

        self.last_press_time = 0.0
        self.callback: Optional[Callable[[], None]] = None

    def set_callback(self, callback: Callable[[], None]):
        """
        Registers a callback function to be called when the button is pressed.
        """
        self.callback = callback
        try:
            GPIO.add_event_detect(Config.BUTTON_GPIO_PIN, GPIO.FALLING, callback=self._handle_press, bouncetime=Config.BUTTON_DEBOUNCE_TIME)
            self.logger.info("Button callback registered.")
        except Exception as e:
            self.logger.error(f"Failed to set button event detect: {e}")

    def _handle_press(self, channel: int):
        now = time.time()
        if (now - self.last_press_time) * 1000 > Config.BUTTON_DEBOUNCE_TIME:
            self.last_press_time = now
            if self.callback:
                self.logger.info("Button pressed, executing callback.")
                try:
                    self.callback()
                except Exception as e:
                    self.logger.error(f"Error in button callback: {e}")

    def cleanup(self):
        """
        Cleans up GPIO event detect and resets GPIO mode.
        Should be called before exiting the program.
        """
        try:
            GPIO.remove_event_detect(Config.BUTTON_GPIO_PIN)
            GPIO.cleanup()
            self.logger.info("Button GPIO cleaned up.")
        except Exception as e:
            self.logger.warn(f"Error during GPIO cleanup: {e}")
