# ---------------------------------------------------------------------------
#   TTS scripts
# ---------------------------------------------------------------------------


def chk_face_greeting(name: str) -> str:
    return "Hello {}!".format(name)


def report_summary_by_child(name: str, ready: int, progress: int, done: int) -> str:
    total = ready + progress + done

    if ready==1:
        script_ready=" {} chore is remaining ".format(ready)
    else: script_ready=" {} chores are remaining ".format(ready)
    
    if progress==1:
        script_progress=" {} chore is in progress ".format(progress)
    else: script_progress=" {} chores are in progress ".format(progress)
    
    if done==1:
        script_done=" and {} chore is completed".format(done)
    else: script_done=" and {} chores are completed".format(done)

    script_1= "Out of {} chores you assigned to {} .".format(
         total, name)
         
    script=script_1+script_ready+script_progress+script_done


    if total == 0:
        script = "You didn't assign any chores to {} today.".format(name)

    if total == 1:
        if ready == 1:
            script = "{} has one chore today, and hasn't started it yet.".format(name)
        if progress == 1:
            script = (
                "{} has one chore today, and its being completed right now.".format(
                    name
                )
            )
        if done == 1:
            script = (
                "{} had one chore today and it's been completed. Well done.".format(
                    name
                )
            )

    return script


def report_allowance(name: str, done: int) -> str:
    return "{} completed all chores, and earned {} dollars today.".format(name, done)


def report_done(name: str) -> str:
    return "There is nothing else to report. Have a good day {}.".format(name)


def do_chore_ready_chore(chore: str = "", count: int = 0, total: int=0) -> str:
    script = "You have {} chores remaining. Your next task is to {}".format(count, chore)
    if count==total:
        script= "It's nice to see you again. Your first chore is to: {} ".format(chore)
    elif count == 0:
        script = "Congraturations! You are done with all of your chores for today. Well done."
    elif count == 1:
        script = "You have one last chore to complete, you need to: {}".format(
            chore
        )
    return script


def do_chore_progress_chore(name: str) -> str:
    return "{}, I know you're doing a chore.".format(name)


def end_chore_progress_chore(chore: str) -> str:
    return "Did you {}?".format(chore)


def end_chore_yes_no() -> str:
    return "Press YES if you completed the chore. Otherwise, press NO."


def end_chore_timeout() -> str:
    return "You didn't press any button. Please try again later."


def end_chore_complete(name: str, done: bool = True) -> str:
    script = "{}, Cheer up! You can do it. I will wait here until you complete your chore".format(name)
    if done == True:
        script = "Well done {}.".format(name)
    return script
