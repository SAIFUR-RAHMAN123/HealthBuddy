class SymptomAgent:
    def simple_rule_based_triage(self, symptoms):
        s = symptoms.lower()
        if any(x in s for x in ["severe","chest pain","unconscious","difficulty breathing"]):
            return "High"
        if any(x in s for x in ["fever","dizziness","fatigue","vomiting"]):
            return "Moderate"
        return "Low"

    def run(self, symptoms):
        risk = self.simple_rule_based_triage(symptoms)
        return {
            "risk": risk,
            "english": "Your symptoms are " + risk,
            "hindi": "आपके लक्षण " + risk + " हैं"
        }
