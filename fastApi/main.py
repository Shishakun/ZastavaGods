import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi import FastAPI, UploadFile

from inputs.yamnetrec import process_audio

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

logger = logging.getLogger(__name__)


@app.get("/yamnet")
async def get_yamnet_result():
    result = process_audio()
    return {"result": result}


@app.post("/facerecognition")
async def recognize_face(image: UploadFile):
    content_type = image.content_type
    if content_type == 'image/jpeg':
        image_bytes = await image.read()
        image_data = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
        face = face_recognition.run_recognition(image)
        if face is not None:
            return JSONResponse(face, status_code=200)
        else:
            return JSONResponse("name or confident not found")
    else:
        return {"error": "Invalid image format. JPEG format is required."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
