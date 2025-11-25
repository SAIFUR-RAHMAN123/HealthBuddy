import pytesseract
from pdf2image import convert_from_path
from PIL import Image

class OCRTool:
    def __init__(self):
        pass

    def run(self, file_path):
        text = ""

        # If PDF
        if file_path.endswith(".pdf"):
            pages = convert_from_path(file_path)
            for page in pages:
                text += pytesseract.image_to_string(page)

        # If image (jpg/png)
        else:
            img = Image.open(file_path)
            text = pytesseract.image_to_string(img)

        return text

ocr_tool = OCRTool()
