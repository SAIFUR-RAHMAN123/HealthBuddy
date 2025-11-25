import json, os
from datetime import datetime

# Optional Gemini wrapper (user can set GEMINI_API_KEY in env)
def gemini_generate(prompt, language="en"):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return ""  # empty => fallback to local rule-based note
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        return ""

# Some simple clinical thresholds (example). These are illustrative, not exhaustive.
THRESHOLDS = {
    "hemoglobin": {"low": 12.0, "high": 18.0, "unit":"g/dL"},
    "wbc": {"low": 4000, "high": 11000, "unit": "cells/uL"},
    "platelets": {"low": 150000, "high": 450000, "unit": "cells/uL"},
    "creatinine": {"low": 0.6, "high": 1.3, "unit":"mg/dL"},
    "tsh": {"low": 0.4, "high": 4.0, "unit":"µIU/mL"},
    "fbs": {"low": 70, "high": 99, "unit":"mg/dL"},
    "ppbs": {"low": 70, "high": 140, "unit":"mg/dL"},
    "hba1c": {"low": 4.0, "high": 5.6, "unit":"%"},
    "amh": {"low": 0.5, "high": 3.5, "unit":"ng/mL"},
    "fs h": {"low": 1.0, "high": 15.0, "unit":""},
    "fsh": {"low": 1.0, "high": 15.0, "unit":""},
    # add more as needed
}

class SummaryAgent:
    def __init__(self, memory_dir="memory"):
        self.memory_dir = memory_dir

    def load_patient(self, patient_id="default"):
        path = os.path.join(self.memory_dir, f"{patient_id}.json")
        if not os.path.exists(path):
            return {}
        return json.load(open(path))

    def detect_abnormal(self, key, info):
        k = key.lower()
        val = info.get("value")
        if val is None:
            return ""
        # exact key match first
        if k in THRESHOLDS:
            t = THRESHOLDS[k]
            if val < t["low"]:
                return "Low"
            if val > t["high"]:
                return "High"
            return "Normal"
        # try partial match
        for tk,t in THRESHOLDS.items():
            if tk in k:
                if val < t["low"]:
                    return "Low"
                if val > t["high"]:
                    return "High"
                return "Normal"
        # fallback to provided flag or empty
        return info.get("flag","")

    def build_report_strings(self, data):
        lines_en = []
        lines_hi = []
        # header
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        lines_en.append(f"Medical Report Summary — {now}\n")
        lines_hi.append(f"मेडिकल रिपोर्ट सारांश — {now}\n")

        doctor_lines = []  # aggregate points for doctor-note

        for key, info in data.items():
            line = f"{key.upper().replace('_',' ')}: {info.get('value','')} {info.get('unit','')}".strip()
            status = self.detect_abnormal(key, info)
            if status:
                line += f"  |  Status: {status}"
            lines_en.append(line)
            lines_en.append("")

            # Hindi simple echo (values same)
            lines_hi.append(line)
            lines_hi.append("")

            # build doctor note bullet
            if status == "Low":
                doctor_lines.append(f"{key.upper()}: LOW (value {info.get('value')})")
            if status == "High":
                doctor_lines.append(f"{key.upper()}: HIGH (value {info.get('value')})")

        # doctor-note (rule-based)
        if doctor_lines:
            dr = "ALERTS FOR DOCTOR:\n" + "\n".join(doctor_lines)
        else:
            dr = "No immediate abnormal alerts detected."

        # try to enhance with Gemini (if user has API)
        enhanced_dr = gemini_generate("Please convert the following doctor note into concise clinical bullet points:\n" + dr, language="en")
        if enhanced_dr:
            doctor_note = enhanced_dr
        else:
            doctor_note = dr

        return "\n".join(lines_en), "\n".join(lines_hi), doctor_note

    def run(self, patient_id="default"):
        data = self.load_patient(patient_id)
        if not data:
            return {"error": "no data"}
        en, hi, doctor_note = self.build_report_strings(data)
        return {"english_summary": en, "hindi_summary": hi, "doctor_note": doctor_note}
