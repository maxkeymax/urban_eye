import io
import os

import cv2
import numpy as np


def generate_preview(file_bytes: bytes) -> bytes:
    """
    Генерирует превью из первого кадра.
    Возвращает (байты превью, имя файла)
    """
    file_bytes_io = io.BytesIO(file_bytes)
    file_bytes_io.seek(0)
    video_data = file_bytes_io.read()

    np_array = np.frombuffer(video_data, dtype=np.uint8)
    tmp_path = "temp_preview.mp4"

    with open(tmp_path, "wb") as f:
        f.write(np_array)

    cap = cv2.VideoCapture(tmp_path)
    ret, first_frame = cap.read()

    if not ret:
        cap.release()
        os.remove(tmp_path)
        raise ValueError("Не удалось извлечь первый кадр")

    _, buffer = cv2.imencode(".jpg", first_frame)
    preview_bytes = buffer.tobytes()

    cap.release()
    os.remove(tmp_path)

    return preview_bytes
