import os
import cv2
import face_recognition
import numpy as np
from loguru import logger
import math
import functools


def face_confidence(face_distance, face_match_threshold=0.6):
    range_val = 1.0 - face_match_threshold
    linear_val = (1.0 - face_distance) / (range_val * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + "%"
    else:
        value = (
            linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))
        ) * 100
        return str(round(value, 2)) + "%"


class FaceRecognition:
    known_face_encodings = []
    known_face_names = []
    face_locations = []
    face_encodings = []
    process_current_frame = None

    @staticmethod
    @functools.lru_cache(maxsize=None)
    def encode_faces():
        people_folders = os.listdir("inputs\people")

        for folder in people_folders:
            folder_path = os.path.join("inputs\people", folder)
            if os.path.isdir(folder_path):
                for image in os.listdir(folder_path):
                    image_path = os.path.join(folder_path, image)
                    try:
                        face_image = face_recognition.load_image_file(image_path)
                        face_encoding = face_recognition.face_encodings(face_image)[0]

                        FaceRecognition.known_face_encodings.append(face_encoding)
                        FaceRecognition.known_face_names.append(folder)
                        logger.debug(folder)
                        logger.debug(image_path)
                    except Exception as e:
                        logger.error("Error processing image: {}".format(image_path))

    @staticmethod
    def detect_faces_in_image(image):
        logger.debug("Изображение принято")
        # Detect faces
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_image)
        logger.debug(face_locations)
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        return face_locations, face_encodings

    @staticmethod
    def run_recognition(image=None):

        if image is not None:
            face_locations, face_encodings = FaceRecognition.detect_faces_in_image(
                image
            )
            if face_locations:
                face_name = {}

                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        FaceRecognition.known_face_encodings, face_encoding
                    )

                    # Initialize name and confidence
                    name = "Неизвестное лицо"
                    confidence = "Неизвестное лицо"

                    # Find matches
                    face_distances = face_recognition.face_distance(
                        FaceRecognition.known_face_encodings, face_encoding
                    )
                    best_match_index = np.argmin(face_distances)

                    # If match found, update name and confidence
                    if matches[best_match_index]:
                        name = FaceRecognition.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

                    logger.debug(name)
                    logger.debug(confidence)

                    FaceRecognition.process_current_frame = (
                        not FaceRecognition.process_current_frame
                    )

                return name

        return None
