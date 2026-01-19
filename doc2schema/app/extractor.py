import os
from typing import Final

import cv2
import pandas as pd
import pdfplumber
import pytesseract
from PIL import Image  # noqa: F401


SUPPORTED_IMAGE_EXTENSIONS: Final = [".png", ".jpg", ".jpeg"]
SUPPORTED_EXCEL_EXTENSIONS: Final = [".xls", ".xlsx"]


def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text_chunks: list[str] = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text_chunks.append(page_text)
        return "\n".join(text_chunks)

    if ext in SUPPORTED_IMAGE_EXTENSIONS:
        img = cv2.imread(file_path)
        if img is None:
            raise ValueError("Failed to read image file")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return pytesseract.image_to_string(gray)

    if ext in SUPPORTED_EXCEL_EXTENSIONS:
        df = pd.read_excel(file_path)
        return df.to_string(index=False)

    if ext == ".csv":
        df = pd.read_csv(file_path)
        return df.to_string(index=False)

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    raise ValueError("Unsupported file type")


