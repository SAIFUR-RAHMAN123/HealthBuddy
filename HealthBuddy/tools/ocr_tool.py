import pytesseract
import fitz  # PyMuPDF
from PIL import Image

class OCRTool:
    def run(self, filepath):
        """Unified OCR method that works for both PDF & Images."""
        text = ""

        # If PDF
        if filepath.lower().endswith(".pdf"):
            try:
                doc = fitz.open(filepath)
                for page in doc:
                    # Direct text extract
                    extracted = page.get_text()
                    if extracted.strip():
                        text += extracted + "\n"
                    else:
                        # Fallback: OCR using image
                        pix = page.get_pixmap()
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        text += pytesseract.image_to_string(img)
                return text
            except Exception as e:
                return f"PDF Error: {str(e)}"

        # If Image
        try:
            img = Image.open(filepath)
            return pytesseract.image_to_string(img)
        except Exception as e:
            return f"Image Error: {str(e)}"


ocr_tool = OCRTool()
