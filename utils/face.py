import os
import logging, time
import face_recognition
import imutils
import pickle
import cv2

from dotenv import load_dotenv
from imutils.video import VideoStream
from imutils.video import FPS


# ---------------------------------------------------------------------------
#   Face recognition model and variables
# ---------------------------------------------------------------------------

load_dotenv()

_model_file = os.environ.get("MODEL_FILE")
_rotate = True if os.environ.get("ROTATE_CAM") == "TRUE" else False
_debug = True if os.environ.get("CV2_WINDOW") == "TRUE" else False

logging.info("Face recognition model: %s", _model_file)
logging.info("Rotate camera: %s", _rotate)
logging.info("CV2 window: %s", _debug)

_data = pickle.loads(open(_model_file, "rb").read())
_unknown = "Unknown"


# ---------------------------------------------------------------------------
#   Detect functions
# ---------------------------------------------------------------------------
#
# Return the first person's name in the name list


def _get_name(names: list) -> str:
    tmp = [n for n in names if n != _unknown]
    return _unknown if len(tmp) == 0 else tmp[0]


#
# Recognize a face and return the first person's name
# Return "Unknown" if the person does not exist in the model file


def recognize(timeout: float = 10) -> str:
    _vs = VideoStream(usePiCamera=True).start()
    time.sleep(2)

    _fps = FPS().start()
    logging.info("Start video stream and fps...")

    start_time = time.time()
    currentname = ""
    names = []

    while time.time() - start_time < timeout and len(names) == 0:
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = _vs.read()
        frame = imutils.resize(frame, width=500)
        if _rotate:
            frame = imutils.rotate(frame, 180)

        # debug
        boxes = []
        encodings = []

        if _debug == True:
            boxes = face_recognition.face_locations(frame)
            encodings = face_recognition.face_encodings(frame, boxes)
        else:
            # compute the facial embeddings for each face bounding box
            encodings = face_recognition.face_encodings(frame)

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(_data["encodings"], encoding)
            name = _unknown  # if face is not recognized, then print Unknown

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = _data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

                # If someone in your dataset is identified, print their name on the screen
                if currentname != name:
                    currentname = name
                    logging.info("Face recognition: %s", currentname)

            # update the list of names
            names.append(name)

        # debug
        if _debug == True:
            for ((top, right, bottom, left), name) in zip(boxes, names):
                # draw the predicted face name on the image - color is in BGR
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 225), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(
                    frame,
                    name,
                    (left, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2,
                )

            # display the image to our screen
            cv2.imshow("Facial Recognition is Running", frame)
            key = cv2.waitKey(1) & 0xFF

            # quit when 'q' key is pressed
            if key == ord("q"):
                break

        # update the FPS counter
        _fps.update()
        time.sleep(0.1)

    # do a bit of cleanup
    _fps.stop()
    logging.info("Elasped time: {:.2f}".format(_fps.elapsed()))
    logging.info("Approx. FPS: {:.2f}".format(_fps.fps()))

    _vs.stop()

    logging.info("Detected faces: %s", names)
    return _get_name(names)
