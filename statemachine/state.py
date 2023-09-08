import abc
import os, sys
import logging

from enum import Enum
from statemachine import speak

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from database.db import DbHandler, UserRole, ChoreStatus
from database.load import get_env
from utils import ultrasonic, buttons, tts, face


# ---------------------------------------------------------------------------
#   The State Enum and Interface
# ---------------------------------------------------------------------------


class State(Enum):
    IDLE = "Idle"
    CHK_FACE = "Check Face"
    REPORT = "Report"
    DO_CHORE = "Do Chore"
    END_CHORE = "End Chore"


class StateInterface(abc.ABC):
    _db = DbHandler(get_env()["db_path"])

    @abc.abstractmethod
    def ready(self) -> None:
        pass

    @abc.abstractmethod
    def process(self) -> None:
        pass

    @abc.abstractmethod
    def done(self) -> State:
        pass


# ---------------------------------------------------------------------------
#   The Working States
# ---------------------------------------------------------------------------
#
# Idle state
# This runs the ultrasonic sensor to see if anyone is in front of the device.
# When the sensor detects something, go to CheckFace state.
#


class IdleState(StateInterface):
    def __init__(self) -> None:
        self._detected = False

    def ready(self) -> None:
        self._detected = False
        pass

    def process(self) -> None:
        # Run the ultrasonic sensor and decide if anything is detected.
        self._detected = ultrasonic.detect_object()

    def done(self) -> State:
        return State.CHK_FACE if self._detected == True else State.IDLE


# CheckFace state
# Run the face recognition. Compare the detected user and users in the database.
# When the detected user is;
# Child -> DoChore state, Parent -> Report state, Unknow -> Idle state.


class CheckFaceState(StateInterface):
    def __init__(self) -> None:
        self._role = UserRole.UNKNOWN

    def ready(self) -> None:
        # Initialize the camera, things for the face recognition, etc.
        pass

    def process(self) -> None:
        # Run face recognition
        name = face.recognize()

        self._role = self._db.get_role_by_user(name)
        if self._role != UserRole.UNKNOWN:
            logging.info("The user: %s, role: %s", name, self._role.name)
            self._db.save_current_user(name)
            tts.play_text(speak.chk_face_greeting(name))
        else:
            logging.info("Unknown user: %s", name)

    def done(self) -> State:
        if self._role == UserRole.CHILD:
            return State.DO_CHORE
        elif self._role == UserRole.PARENT:
            return State.REPORT
        else:
            return State.IDLE


# Report state
# Fetch and summary the chore status. Then, report it using TTS.
# After TTS, go to Idle state.


class ReportState(StateInterface):
    def __init__(self) -> None:
        pass

    def ready(self) -> None:
        pass

    def process(self) -> None:
        children = self._db.get_children()
        for child in children:
            name = child["name"]
            ready = self._db.count_chores_by_user(name, ChoreStatus.READY)
            progress = self._db.count_chores_by_user(name, ChoreStatus.IN_PROGRESS)
            done = self._db.count_chores_by_user(name, ChoreStatus.DONE)

            logging.info(
                "Summary: %s, ready %d, progress %d, done %d",
                name,
                ready,
                progress,
                done,
            )
            tts.play_text(speak.report_summary_by_child(name, ready, progress, done))

            if done != 0 and ready == 0 and progress == 0:
                tts.play_text(speak.report_allowance(name, done))

        user = self._db.get_current_user()
        tts.play_text(speak.report_done(user))

    def done(self) -> State:
        return State.IDLE


# DoChore state
# Read the current user from the database. Read the chore status of the user.
# When there is a progress chore, go to EndChore state.
# When there is no progress and at least a ready chore, run TTS and then go to Idle state.
# When no progress nor ready chore, run TTS and go to Idle state.


class DoChoreState(StateInterface):
    def __init__(self) -> None:
        self._script = ""
        self._next = State.IDLE

    def ready(self) -> None:
        user = self._db.get_current_user()
        if self._db.get_progress_chore_by_user(user) != None:
            self._script = speak.do_chore_progress_chore(user)
            self._next = State.END_CHORE
            return


        #Count total number of chores
        ready = self._db.count_chores_by_user(user, ChoreStatus.READY)
        progress = self._db.count_chores_by_user(user, ChoreStatus.IN_PROGRESS)
        done = self._db.count_chores_by_user(user, ChoreStatus.DONE)
        total_chores=ready+progress+done
        #Get the chores remaining to do
        ready_chores = self._db.get_ready_chores_by_user(user)

        if len(ready_chores) == 0:
            self._script = speak.do_chore_ready_chore()
        else:
            chore = ready_chores[0]
            self._db.update_chore_status_by_id(chore.doc_id, ChoreStatus.IN_PROGRESS)
            self._script = speak.do_chore_ready_chore(chore["task"], len(ready_chores),total_chores)

        self._next = State.IDLE

    def process(self) -> None:
        tts.play_text(self._script)
        pass

    def done(self) -> State:
        return self._next


# End Chore state
# Check the progress chore, handle the hardware button click, and update the database.
# After everything is done, go to Idle state.


class EndChoreState(StateInterface):
    def __init__(self) -> None:
        self._script = ""
        self._user = ""
        self._chore = None

    def ready(self) -> None:
        self._user = self._db.get_current_user()
        self._chore = self._db.get_progress_chore_by_user(self._user)

        if self._chore == None:
            logging.error("No IN_PROGRESS chore for %s. Go to IDLE state.", self._user)
        else:
            self._script = speak.end_chore_progress_chore(self._chore["task"])

    def process(self) -> None:
        # Run TTS using self._script and script
        tts.play_text(self._script)
        tts.play_text(speak.end_chore_yes_no())

        # Handle the hardware buttons
        btn_state = buttons.get_button_pressed(10)

        if btn_state == buttons.ButtonState.YES:
            self._db.update_chore_status_by_id(self._chore.doc_id, ChoreStatus.DONE)
            self._script = speak.end_chore_complete(self._user)
            ready = self._db.count_chores_by_user(self._user, ChoreStatus.READY)
            if ready==0:
                self._next = State.IDLE
            else: 
                self._next = State.DO_CHORE
            
        elif btn_state == buttons.ButtonState.NO:
            self._script = speak.end_chore_complete(self._user, done=False)
            self._next = State.IDLE
        else:
            self._script = speak.end_chore_timeout()
            self._next = State.IDLE
        tts.play_text(self._script)

    def done(self) -> State:
        return self._next 
