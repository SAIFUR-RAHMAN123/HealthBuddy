import json
import os
from datetime import datetime
from tools.ocr_tool import ocr_tool
from tools.parser_tool import parser_tool

class IngestAgent:
    def __init__(self, memory_dir="memory"):
        self.memory_dir = memory_dir
        os.makedirs(self.memory_dir, exist_ok=True)

    def run(self, file_path, patient_id="default"):
        # 1. OCR and parse
        text = ocr_tool.run(file_path)
        structured = parser_tool.parse(text)

        # 2. Save latest snapshot (overwrite patient.json for current state)
        memory_path = os.path.join(self.memory_dir, f"{patient_id}.json")
        with open(memory_path, "w") as f:
            json.dump(structured, f, indent=4)

        # 3. Append time-series history
        history_path = os.path.join(self.memory_dir, f"{patient_id}_history.json")
        snapshot = {
            "timestamp": datetime.utcnow().isoformat(),
            "data": structured
        }

        if os.path.exists(history_path):
            with open(history_path, "r") as f:
                hist = json.load(f)
        else:
            hist = []

        hist.append(snapshot)
        with open(history_path, "w") as f:
            json.dump(hist, f, indent=4)

        return structured
