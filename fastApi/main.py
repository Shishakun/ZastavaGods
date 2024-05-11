import asyncio
import base64
import io
from pathlib import Path

import psycopg2
import pyaudio
import uvicorn
from PIL import Image
from fastapi import FastAPI, Form, File, UploadFile, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from inputs.facerecognition import *
from inputs.yamnetrec import process_audio
from inputs.yolo_connet import *

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

FaceRecognition.encode_faces()


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


# Define class font and colors if needed
class_font = cv2.FONT_HERSHEY_SIMPLEX
class_font_scale = 1
class_colors = {0: (255, 0, 0), 1: (0, 255, 0), 2: (0, 0, 255), 3: (255, 255, 0)}


async def detection():
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    capture.set(cv2.CAP_PROP_POS_MSEC, 100)
    if not capture.isOpened():
        print(capture)
        raise Exception("Failed to open the capture device")

    class_labels = ["MilitaryVehicle", "People", "car", "drone"]
    while True:
        ret, frame = capture.read()

        if ret:
            ret, buffer = cv2.imencode('.jpg', frame)
            if torch.cuda.is_available():
                result = model(frame, device=0)
            else:
                result = model(frame, conf=0.3)

            for result_item in result[0]:
                if result_item is not None and len(result_item) >= 6:
                    boxes = result_item[:, :4].cpu().numpy()
                    classes = result_item[:, 5].cpu().numpy()
                    confidences = result_item[:, 4].cpu().numpy()

                    for box, cls, conf in zip(boxes, classes, confidences):
                        x1, y1, x2, y2 = box.astype(int)
                        cls = int(cls)
                        conf = round(float(conf), 2)

                        label = class_labels[cls] + str(conf)
                        box_color = class_colors.get(cls, (255, 255, 255))

                        (label_width, label_height), _ = cv2.getTextSize(
                            label, class_font, class_font_scale, 1
                        )
                        text_position = (x1, y1 - 3 - label_height)

                        cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                        cv2.putText(
                            frame,
                            label,
                            text_position,
                            class_font,
                            class_font_scale,
                            box_color,
                            2,
                        )

            _, jpeg = cv2.imencode(".jpg", frame)
            frame_bytes = jpeg.tobytes()
            await asyncio.sleep(0.03)
            yield base64.b64encode(frame_bytes)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    async for frame_bytes in detection():
        await websocket.send_bytes(frame_bytes)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
