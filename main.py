import logging, logging.config
from time import sleep

# logging configuration
logging.config.fileConfig("logging.conf")


# ---------------------------------------------------------------------------
#   Initialize DB
#   - Delete the existing database json and create a new one using the yml.
# ---------------------------------------------------------------------------

from database.load import initialize_db

initialize_db()


# ---------------------------------------------------------------------------
#   State Machine
# ---------------------------------------------------------------------------

from statemachine.state import (
    State,
    IdleState,
    CheckFaceState,
    ReportState,
    DoChoreState,
    EndChoreState,
)


class StateMachine:
    def __init__(self):
        self._state = State.IDLE
        self._action = IdleState()

    def _next(self, next_state: State) -> None:
        logging.info("[%s] => [%s]" % (self._state, next_state))
        self._state = next_state

        if self._state == State.IDLE:
            self._action = IdleState()
        elif self._state == State.CHK_FACE:
            self._action = CheckFaceState()
        elif self._state == State.REPORT:
            self._action = ReportState()
        elif self._state == State.DO_CHORE:
            self._action = DoChoreState()
        elif self._state == State.END_CHORE:
            self._action = EndChoreState()
        else:
            logging.error("Unknown State: %s", self._state)

    def run(self) -> None:
        self._action.ready()
        self._action.process()
        next_state = self._action.done()
        self._next(next_state)


def main():
    machine = StateMachine()

    while True:
        machine.run()
        sleep(1)


if __name__ == "__main__":
    main()
