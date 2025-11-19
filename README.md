**📘 HealthBuddy — AI Multi-Agent Healthcare Assistant**
Personal Medical Report Analyzer + Symptom Triage + Personalized Health Tips

HealthBuddy is an AI-powered multi-agent healthcare assistant designed to simplify medical reports, analyze symptoms, and give personalized health recommendations — all in English + Hindi.

This project is developed as part of the Google 5-Day AI Agents Intensive Course.




**🚑 1. Problem Statement**

Millions of patients struggle with:
 * Medical reports they cannot understand
 * No proper summary of past health data
 * Confusion about whether their symptoms are serious
 * No personalized health tips based on lab reports
 * Multiple doctors → many prescriptions → no unified record

This results in poor health awareness, delayed treatment, and miscommunication.

**🤖 2. Solution — HealthBuddy**
HealthBuddy is a multi-agent healthcare assistant that:

🧠 1. Reads & extracts data from ANY lab report
 * Automates OCR (PDF/Image → Text)
 * Parses CBC, LFT, KFT, Thyroid, Hormones, Vitamin, Sugar tests, etc.

📊 2. Creates human-readable medical summaries
 * Clean English summary
 * Clean Hindi summary
 * Report-style output (PDF-like)

🩺 3. Analyzes symptoms
 * Low / Moderate / High risk triage
 * English + Hindi advice
 * When to see a doctor

❤️ 4. Gives personalized health tips
 * Based on medical history
 * Lifestyle suggestions
 * Follow-up reminders

💾 5. Stores patient history
 * Memory saved in JSON
 * Multiple uploads over time
 * Useful for long-term tracking




**🧩 3. Multi-Agent Architecture**

            ┌─────────────────────┐
            │     User Upload      │
            └──────────┬──────────┘
                       │
                       ▼
       ┌────────────────────────────────────┐
       │           Ingest Agent             │
       │ OCR → Parser → Memory Save         │
       └───────────────┬────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │           Summary Agent         │
        │   English + Hindi Summaries     │
        └─────────────────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │          Symptom Agent          │
        │  Risk Triage + Multilingual     │
        └─────────────────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │          Tips Agent             │
        │ Personalized Tips + Reminders   │
        └─────────────────────────────────┘

This architecture ensures modular, scalable, and maintainable agent behavior.





**🧠 4. Key Concepts Used **
 ✔ Multi-Agent System
 ✔ Sequential Agents
 ✔ Loop Agents (Iterative parsing)
 ✔ Tools: OCR Tool, Parser Tool
 ✔ Custom Tools (ParserTool, OCRTool)
 ✔ Memory (Per-patient JSON)
 ✔ State Management
 ✔ Context Engineering (clean summaries)
 ✔ Observability (print sections)
 ✔ Agent Evaluation through test cells





**⚙️ 5. Project Features**
✔ Upload any lab report (PDF/JPG/PNG)
✔ Universal medical parser (CBC, LFT, KFT, Thyroid, Hormones, Vitamins, Sugar tests)
✔ English + Hindi output
✔ Human-readable summaries
✔ Personalized health tips
✔ Symptom triage
✔ Real-time suggestions




**📁 6. Project Structure**
HealthBuddy/
│
├── agents/
│   ├── ingest_agent.py
│   ├── summary_agent.py
│   ├── symptom_agent.py
│   ├── tips_agent.py
│   └── orchestrator.py
│
├── tools/
│   ├── ocr_tool.py
│   └── parser_tool.py
│
├── memory/
│   ├── user1.json
│
├── data/
│   ├── sample_report.pdf (optional)
│
├── HealthBuddy.ipynb  <-- Final cleaned notebook
└── README.md





**🚀 7. How to Run (Colab)**
 1. Open HealthBuddy.ipynb
 2. Run the install libraries cell
 3. Run folder creation
 4. Upload PDF report
 5. Run OCR + Parser
 6. Run all Agents
 7. Use Orchestrator
 8. See final formatted output




**🧪 8. Sample Usage (Orchestrator)**
orc = HealthAgentOrchestrator()
orc.run("upload_report", file_path="report.pdf", patient_id="user1")
orc.run("summary", patient_id="user1")
orc.run("symptoms", text="dizziness and headache")
orc.run("tips", patient_id="user1")





**🎬 9. Video Demo (3-minute Script)**

   ---------





**🔮 10. Future Improvements**
* Gemini 2.0 Flash for medical LLM reasoning
* Doctor-prescription summarizer
* Multi-user cloud database
* Chat conversational mode
* Integration with Google Fit / wearable data
* Dashboard with charts





**⚠️ 11. Disclaimer**
HealthBuddy is not a medical device.
Always consult a qualified doctor for medical decisions.




**👨‍💻 Author**
Saifur Rahman
AI Developer | Google AI Agents Course Participant
