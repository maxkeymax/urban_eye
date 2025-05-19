# urban_eye/services/metadata_extractor.py

import cv2
import tempfile
import os
from typing import Dict


def extract_video_metadata(file_bytes: bytes) -> Dict[str, any]:
    """
    Извлекает метаданные видео из байтовой строки.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    cap = cv2.VideoCapture(tmp_path)
    if not cap.isOpened():
        os.remove(tmp_path)
        raise ValueError("Не удалось открыть видео")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps != 0 else 0

    cap.release()
    os.remove(tmp_path)

    return {
        "fps": fps,
        "frame_count": frame_count,
        "width": width,
        "height": height,
        "duration_sec": duration,
        "video_resolution": f"{width}x{height}"
    }
    