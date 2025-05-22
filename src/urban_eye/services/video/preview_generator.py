import os
import tempfile
from typing import Tuple

import cv2


def generate_preview(file_bytes: bytes) -> Tuple[bytes, str]:
    """
    Генерирует превью из первого кадра.
    Возвращает (байты превью, имя файла)
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

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

    return preview_bytes, "preview.jpg"
