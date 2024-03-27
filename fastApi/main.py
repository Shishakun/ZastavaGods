import uvicorn
import base64
import io
import numpy as np
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from loguru import logger
from inputs.yamnetrec import process_audio
from pydantic import BaseModel
from inputs.facerecognition import *

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


class ImageRequest(BaseModel):
    image: str


@app.get("/yamnet")
async def get_yamnet_result():
    result = process_audio()
    return {"result": result}


@app.post("/facerecognition")
async def upload_image(image_data: ImageRequest):
    try:
        image = image_data.image.split(",")[1]

        image_bytes = base64.b64decode(image)

        img = Image.open(io.BytesIO(image_bytes))
        img_array = np.array(img)
        face_recognition = FaceRecognition()
        face = face_recognition.run_recognition(img_array)

        response_data = {"message": face}
        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        logger.error(str(e))
        return JSONResponse(
            content={"message": "An error occurred during face recognition"},
            status_code=500,
        )


class User(BaseModel):
    surname: str
    name: str
    patronymic: str
    otdel: str
    secret: int


@app.post("/uploadPeople")
async def create_user(user: User):
    # Делайте что-то с полученными данными
    return {"message": "Данные успешно получены и обработаны"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
