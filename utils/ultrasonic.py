import os
import logging

from gpiozero import DistanceSensor
from dotenv import load_dotenv


# ---------------------------------------------------------------------------
#   Load environment variables
# ---------------------------------------------------------------------------

load_dotenv()

_trigger_pin = os.environ.get("ULTRASONIC_TRIG_PIN")
_echo_pin = os.environ.get("ULTRASONIC_ECHO_PIN")
_sensor = DistanceSensor(echo=_echo_pin, trigger=_trigger_pin)

logging.info("Ultrasonic GPIO pins trigger: %s, echo: %s" % (_trigger_pin, _echo_pin))


# ---------------------------------------------------------------------------
#   Ultrasonic sensor
# ---------------------------------------------------------------------------


def detect_object(distance: float = 65) -> bool:
    cm = _sensor.distance * 100
    logging.info("Distance: %.2f cm", cm)
    return True if cm < distance else False
