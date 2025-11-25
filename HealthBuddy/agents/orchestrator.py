from agents.ingest_agent import IngestAgent
from agents.summary_agent import SummaryAgent
from agents.symptom_agent import SymptomAgent
from agents.tips_agent import TipsAgent

class HealthAgentOrchestrator:
    def __init__(self):
        self.ingest = IngestAgent()
        self.summary = SummaryAgent()
        self.symptom = SymptomAgent()
        self.tips = TipsAgent()

    def run(self, action, **kwargs):
        if action == "upload_report":
            return self.ingest.run(kwargs["file_path"], kwargs.get("patient_id","user1"))
        if action == "summary":
            return self.summary.run(kwargs.get("patient_id","user1"))
        if action == "symptoms":
            return self.symptom.run(kwargs["text"])
        if action == "tips":
            return self.tips.run(kwargs.get("patient_id","user1"))
        return {"error": "Invalid action"}
