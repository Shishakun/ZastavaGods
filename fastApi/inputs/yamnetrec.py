import Yamnet.yamnet.params as params
import Yamnet.yamnet.yamnet as yamnet_model
import pyaudio
import librosa
import numpy as np
from loguru import logger


def process_audio():
    yamnet = yamnet_model.yamnet_frames_model(params)
    yamnet.load_weights("Yamnet/yamnet/yamnet.h5")
    yamnet_classes = yamnet_model.class_names("Yamnet/yamnet/yamnet_class_map.csv")

    frame_len = int(params.SAMPLE_RATE * 2)  # 1sec

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=params.SAMPLE_RATE,
        input=True,
        frames_per_buffer=frame_len,
    )
    result = []
    while True:
        # data read
        data = stream.read(frame_len, exception_on_overflow=False)

        # byte --> float
        frame_data = librosa.util.buf_to_float(data, n_bytes=2, dtype=np.int16)

        # model prediction
        scores = yamnet.predict(np.reshape(frame_data, [1, -1]), steps=1)
        prediction = np.mean(scores, axis=0)

        top5_i = np.argsort(prediction)[::-1][:2]

        # append result to list
        current_event = "; ".join(
            "{:12s}:{:.3f}".format(yamnet_classes[i], prediction[i]) for i in top5_i
        )
        result.append(current_event)
        return result

    stream.stop_stream()
    stream.close()
    p.terminate()
