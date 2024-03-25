import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi import FastAPI, UploadFile
from loguru import logger
from inputs.yamnetrec import process_audio
import numpy as np
import io
from PIL import Image
import base64
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


@app.get("/yamnet")
async def get_yamnet_result():
    result = process_audio()
    return {"result": result}


@app.post("/facerecognition")
async def upload_image(image: dict):
    # image_data = io.BytesIO(base64.b64decode(image.split(",")[1]))
    # img = Image.open(image_data)
    # img_array = np.array(img)
    # # Process the image with the FaceRecognition class
    # face_recognition = FaceRecognition()
    # face = face_recognition.run_recognition(img_array)
    # if face is not None:
    #     return JSONResponse(face, status_code=200)
    # else:
    #     return JSONResponse("name or confident not found")
    return {"message": "Принято"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
