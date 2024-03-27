import os
import cv2
import face_recognition
import numpy as np
from loguru import logger
import math


def face_confidence(face_distance, face_match_threshold=0.6):
    range = 1.0 - face_match_threshold
    linear_val = (1.0 - face_distance) / (range * 2.0)

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
    def __init__(self):
        self.face_encoding = None
        self.process_current_frame = None
        self.encode_faces()
        # Load known faces
        self.face_locations = []
        self.face_encodings = []

    def encode_faces(self):
        # Load images from 'people' directory
        for image in os.listdir("./inputs/people"):
            try:
                face_image = face_recognition.load_image_file(
                    f"./inputs/people/{image}"
                )
                self.face_encoding = face_recognition.face_encodings(face_image)[0]

                self.known_face_encodings.append(self.face_encoding)

                self.known_face_names.append(image)
            except Exception as e:
                logger.error("Локалка пуста")

    def detect_faces_in_image(self, image):
        logger.debug("Изображение принято")
        # Detect faces
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.face_locations = face_recognition.face_locations(rgb_image)
        logger.debug(self.face_locations)
        self.face_encodings = face_recognition.face_encodings(
            rgb_image, self.face_locations
        )
        return self.face_locations, self.face_encodings

    def run_recognition(self, image=None):

        if image is not None:
            self.face_locations, self.face_encodings = self.detect_faces_in_image(image)
            if self.face_locations:
                face_name = {}

                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(
                        self.known_face_encodings, face_encoding
                    )

                    # Initialize name and confidence
                    name = "Неизвестное лицо"
                    confidence = "Неизвестное лицо"

                    # Find matches
                    face_distances = face_recognition.face_distance(
                        self.known_face_encodings, face_encoding
                    )
                    best_match_index = np.argmin(face_distances)

                    # If match found, update name and confidence
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

                    logger.debug(name)
                    logger.debug(confidence)


                    self.process_current_frame = not self.process_current_frame

                return name

        return None
