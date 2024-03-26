import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile
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
    image = image_data.image
    return {"message": "Принято"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
