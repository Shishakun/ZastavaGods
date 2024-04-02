import uvicorn
import base64
import io
import numpy as np
import psycopg2
import pyaudio
from PIL import Image
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import JSONResponse
from loguru import logger
from inputs.yamnetrec import process_audio
from pydantic import BaseModel
from inputs.facerecognition import *
from fastapi.staticfiles import StaticFiles

face_recognition = FaceRecognition()
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/inputs/people", StaticFiles(directory="inputs/people"), name="people")


class ImageRequest(BaseModel):
    image: str


@app.get("/yamnet")
async def get_yamnet_result():
    result = process_audio()
    return {"result": result}


@app.get("/yamnetgraph")
async def get_graph():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        # Здесь обработайте аудиоданные и анализируйте их частоту

    stream.stop_stream()
    stream.close()
    p.terminate()


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


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
