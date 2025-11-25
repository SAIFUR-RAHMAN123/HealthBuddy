import json, os

class TipsAgent:
    def run(self, patient_id="default"):
        path = os.path.join("memory", f"{patient_id}.json")
        data = json.load(open(path))

        return {
            "tips": [
                "Drink water",
                "Walk daily",
                "Sleep well"
            ]
        }
