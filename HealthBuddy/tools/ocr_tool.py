import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import numpy as np

class OCRTool:
    def extract_text(self, filepath):
        """Extracts text from both PDF and Images using PyMuPDF + OCR."""
        text = ""

        # Case 1: PDF
        if filepath.lower().endswith(".pdf"):
            try:
                doc = fitz.open(filepath)
                for page in doc:
                    text += page.get_text()  # Direct extraction
                    # If page has no text, use OCR
                    if len(page.get_text().strip()) < 10:
                        pix = page.get_pixmap()
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        text += pytesseract.image_to_string(img)
                return text

            except Exception as e:
                return f"PDF OCR Error: {e}"

        # Case 2: Image
        try:
            img = Image.open(filepath)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            return f"Image OCR Error: {e}"


ocr_tool = OCRTool()
