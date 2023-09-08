import os
import time
import logging

from enum import Enum
from gpiozero import Button
from dotenv import load_dotenv


# ---------------------------------------------------------------------------
#   Load environment variables
# ---------------------------------------------------------------------------

load_dotenv()

_yes_pin = os.environ.get("BUTTON_YES_PIN")
_no_pin = os.environ.get("BUTTON_NO_PIN")

logging.info("Tactile button pins Yes: %s, No: %s" % (_yes_pin, _no_pin))


# ---------------------------------------------------------------------------
#   The Button State Enum
# ---------------------------------------------------------------------------


class ButtonState(Enum):
    YES = "yes"
    NO = "no"
    NONE = "none"


_STATE = ButtonState.NONE


def _button_yes_pressed():
    global _STATE
    logging.debug("Button YES pressed.")
    _STATE = ButtonState.YES


def _button_no_pressed():
    global _STATE
    logging.debug("Button NO pressed.")
    _STATE = ButtonState.NO


_button_yes = Button(_yes_pin)
_button_no = Button(_no_pin)

_button_yes.when_pressed = _button_yes_pressed
_button_no.when_pressed = _button_no_pressed


# ---------------------------------------------------------------------------
#   The Tactile Buttons
# ---------------------------------------------------------------------------


def get_button_pressed(timeout: float = 10) -> ButtonState:
    global _STATE
    _STATE = ButtonState.NONE
    state = _STATE

    start_time = time.time()
    while time.time() - start_time < timeout:
        if _STATE != ButtonState.NONE:
            state = _STATE
            break
        time.sleep(0.5)

    logging.info("Tactile button status: %s", state)
    return state
