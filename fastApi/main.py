import asyncio
import base64
import io
import os
from pathlib import Path

import psycopg2
import numpy as np
import pyaudio
import cv2
import uvicorn
from loguru import logger
from PIL import Image
from fastapi import FastAPI, Form, File, UploadFile, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.websockets import WebSocketDisconnect
from websockets import ConnectionClosed

from inputs.facerecognition import *
from inputs import yamnetrec
from inputs.yamnetrec import *
from inputs.yolo_connet import *

app = FastAPI()
face_recognition = FaceRecognition()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/inputs/people", StaticFiles(directory="inputs/people"), name="people")


FaceRecognition.encode_faces()


class ImageRequest(BaseModel):
    image: str


@app.websocket("/ws/yamnet")
async def yamnet_stream(websocket: WebSocket):
    await websocket.accept()
    yamnetrec.start_processing()
    try:
        while True:
            if yamnetrec.processing:
                result = yamnetrec.get_latest_result()
                await websocket.send_text(result)
                await asyncio.sleep(2)  # Отправка данных каждые 2 секунды
            else:
                await asyncio.sleep(0.1)  # Проверяем состояние каждые 100 мс
    except (WebSocketDisconnect, ConnectionClosed):
        yamnetrec.stop_processing()
        print("Client disconnected")


@app.get("/getperson")
async def get_person():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Zastava",
            user="postgres",
            password="59uranuv",
        )
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        # Выполнение SQL-запроса для получения информации о пользователе по пути
        cursor.execute(f"SELECT * FROM people")
        people = []
        for row in cursor.fetchall():
            people.append(
                {
                    "id": row[0],
                    "surname": row[1],
                    "name": row[2],
                    "patronymic": row[3],
                    "otdel": row[4],
                    "secret": row[5],
                    "image_path": row[6],
                }
            )
        # Закрытие курсора и соединения с базой данных
        logger.debug(people)
        cursor.close()
        conn.close()
        return {"people": people, "total_count": len(people)}

    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"message": "An error occurred during face recognition"},
            status_code=500,
        )


@app.delete("/deleteperson/{person_id}")
async def delete_person(person_id: int):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="Zastava",
            user="postgres",
            password="59uranuv",
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM people WHERE id = %s", (person_id,))
        person_data = cursor.fetchone()
        if not person_data:
            raise HTTPException(status_code=404, detail="Person not found")
        surname, name, patronymic = person_data[1], person_data[2], person_data[3]
        people_dir = f"inputs/people/{surname}_{name}_{patronymic}"
        cursor.execute("DELETE FROM people WHERE id = %s", (person_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Person not found")
        conn.commit()
        cursor.close()
        conn.close()

        # Удаление папки и файлов, связанных с персоной
        if os.path.exists(people_dir):
            for file_name in os.listdir(people_dir):
                file_path = os.path.join(people_dir, file_name)
                os.remove(file_path)
            os.rmdir(people_dir)

        return {"message": "Person deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/facerecognition")
async def upload_image(image_data: ImageRequest):
    try:
        image = image_data.image.split(",")[1]

        image_bytes = base64.b64decode(image)

        img = Image.open(io.BytesIO(image_bytes))
        img_array = np.array(img)
        face_recognition = FaceRecognition()

        face = face_recognition.run_recognition(img_array)
        path_acc = Path.cwd().joinpath("inputs").joinpath("people").joinpath(face)
        for image in path_acc.iterdir():
            image_path_acc = "\\" + face + "\\" + image.name
        logger.debug(image_path_acc)
        conn = psycopg2.connect(
            host="localhost",
            database="Zastava",
            user="postgres",
            password="59uranuv",
        )
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        # Выполнение SQL-запроса для получения информации о пользователе по пути
        cursor.execute(f"SELECT * FROM people WHERE photo_path='{image_path_acc}'")
        user_data = cursor.fetchone()
        logger.debug(user_data)
        # Закрытие курсора и соединения с базой данных
        cursor.close()
        conn.close()

        if user_data is not None:
            surname = user_data[1]
            name = user_data[2]
            patronymic = user_data[3]
            otdel = user_data[4]
            secret = user_data[5]
            image_path = user_data[6]
            response_data = {
                "message": {
                    "surname": surname,
                    "name": name,
                    "patronymic": patronymic,
                    "otdel": otdel,
                    "secret": secret,
                    "image_path": image_path,
                }
            }
            return JSONResponse(content=response_data, status_code=200)
    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"message": "An error occurred during face recognition"},
            status_code=500,
        )


@app.post("/uploadPeople")
async def submit_person_data(
    surname: str = Form(...),
    name: str = Form(...),
    patronymic: str = Form(...),
    otdel: str = Form(...),
    secret: int = Form(...),
    file: UploadFile = File(...),
):
    # Create a directory for the photo
    people_dir = f"inputs\people\{surname}_{name}_{patronymic}"
    os.makedirs(people_dir, exist_ok=True)

    # Save the photo
    file_path = os.path.join(people_dir, file.filename)
    logger.debug(file_path)
    with open(file_path, "wb") as f:
        while True:
            chunk = file.file.read(8192)
            if not chunk:
                break
            f.write(chunk)
    foto_path = f"\{surname}_{name}_{patronymic}\{file.filename}"
    logger.debug(foto_path)
    # Сохранение данных в PostgreSQL с использованием psycopg2
    conn = psycopg2.connect("dbname=Zastava user=postgres password=59uranuv")
    logger.debug(f"Connected to database!")
    cur = conn.cursor()
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS people (
                id SERIAL PRIMARY KEY,
                surname VARCHAR(255),
                name VARCHAR(255),
                patronymic VARCHAR(255),
				otdel VARCHAR(255),
                secret VARCHAR(255),
                photo_path VARCHAR(255)
            )
        """
    )
    cur.execute(
        "INSERT INTO people (surname, name, patronymic, otdel, secret, photo_path) VALUES (%s, %s, %s, %s, %s, %s)",
        (surname, name, patronymic, otdel, secret, foto_path),
    )
    cur.execute("SELECT  *  FROM people")
    rows = cur.fetchall()
    logger.debug(rows)
    conn.commit()
    return {"message": "Данные успешно получены и обработаны"}


@app.websocket("/ws")
async def get_stream(websocket: WebSocket):
    await websocket.accept()
    try:

        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        # object classes
        class_names = ["MilitaryVehicle", "People", "car", "drone"]
        data = []
        while True:
            success, img = cap.read()
            results = model(img, stream=True)

            # coordinates
            for r in results:
                boxes = r.boxes

                for box in boxes:
                    # bounding box
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = (
                        int(x1),
                        int(y1),
                        int(x2),
                        int(y2),
                    )  # convert to int values

                    # put box in cam
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 1)

                    # confidence
                    confidence = math.ceil((box.conf[0] * 100)) / 100
                    print("Confidence --->", confidence)

                    # class name
                    cls = int(box.cls[0])
                    print("Class name -->", class_names[cls])

                    # object details
                    org = [x1, y1]
                    font = cv2.FONT_HERSHEY_DUPLEX
                    fontScale = 0.4
                    color = (0, 0, 0)
                    thickness = 1

                    cv2.putText(
                        img, class_names[cls], org, font, fontScale, color, thickness
                    )

                    cropped_img = img[y1:y2, x1:x2]

                    _, cropped_jpeg = cv2.imencode(".jpg", cropped_img)
                    cropped_frame_bytes = cropped_jpeg.tobytes()
                    cropped_frame_base64 = base64.b64encode(cropped_frame_bytes).decode(
                        "utf-8"
                    )

                    data.append(
                        {
                            "class": class_names[cls],
                            "confidence": confidence,
                            "bounding_box": [x1, y1, x2, y2],
                            "cropped_image": cropped_frame_base64,
                        }
                    )
                    await websocket.send_json(data)

                _, jpeg = cv2.imencode(".jpg", img)
                frame_bytes = jpeg.tobytes()
                frame_base64 = base64.b64encode(frame_bytes).decode("utf-8")

                message = {"message": data, "image": frame_base64}

                await websocket.send_json(message)

                await asyncio.sleep(0.03)
    except (WebSocketDisconnect, ConnectionClosed):
        print("Client disconnected")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
