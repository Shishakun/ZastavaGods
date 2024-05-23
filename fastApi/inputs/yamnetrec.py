import Yamnet.yamnet.params as params
import Yamnet.yamnet.yamnet as yamnet_model
import pyaudio
import librosa
import csv
import numpy as np
from loguru import logger
import threading

yamnet = None
stream = None
latest_result = None
processing = False
yamnet_classes = None


def load_model():
    global yamnet, yamnet_classes
    yamnet = yamnet_model.yamnet_frames_model(params)
    yamnet.load_weights("Yamnet/yamnet/yamnet.h5")
    with open(
        "Yamnet/yamnet/yamnet_class_map.csv", newline="", encoding="utf-8"
    ) as csvfile:
        yamnet_classes = [row["display_name"] for row in csv.DictReader(csvfile)]


def process_audio():
    global stream, latest_result, processing
    frame_len = int(params.SAMPLE_RATE * 2)  # 2 секунды

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=params.SAMPLE_RATE,
        input=True,
        frames_per_buffer=frame_len,
    )

    while processing:
        try:
            data = stream.read(frame_len, exception_on_overflow=False)
            frame_data = librosa.util.buf_to_float(data, n_bytes=2, dtype=np.int16)
            scores = yamnet.predict(np.reshape(frame_data, [1, -1]), steps=1)
            prediction = np.mean(scores, axis=0)
            top5_i = np.argsort(prediction)[::-1][:2]
            current_event = "; ".join(
                "{:12s}:{:.3f}".format(yamnet_classes[i], prediction[i]) for i in top5_i
            )
            latest_result = current_event
        except Exception as e:
            logger.error(e)
            break

    stream.stop_stream()
    stream.close()
    p.terminate()


def start_processing():
    global processing
    if not processing:
        processing = True
        threading.Thread(target=process_audio).start()


def stop_processing():
    global processing
    processing = False


def get_latest_result():
    global latest_result
    return latest_result if latest_result else "No result available"


load_model()
