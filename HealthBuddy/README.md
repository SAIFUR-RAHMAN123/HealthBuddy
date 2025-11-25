# 📘 HealthBuddy — AI Multi-Agent Healthcare Assistant (with Web Dashboard)

**Personal Medical Report Analyzer + Symptom Triage + Personalized Health Tips + Web Dashboard**

HealthBuddy is an AI-powered multi-agent healthcare assistant designed to:

- Simplify medical reports  
- Analyze symptoms  
- Give personalized health recommendations  
- Provide a real-time **web dashboard** to interact with your data  
- Support **English + Hindi**  



---

## 🚑 1. Problem Statement

Millions of patients struggle with:

- Medical reports they cannot understand  
- No proper summary of past health data  
- Confusion about whether their symptoms are serious  
- No personalized health tips based on lab reports  
- Multiple doctors → many prescriptions → no unified record  

This results in poor health awareness, delayed treatment, and miscommunication.

---

## 🤖 2. Solution — HealthBuddy

**HealthBuddy** is a multi-agent healthcare assistant with a **Streamlit-based dashboard** and **Google Gemini–powered reasoning** that:

### 🧠 1. Reads & extracts data from ANY lab report
- OCR for PDFs / Images (PDF, JPG, PNG)
- Parses CBC, LFT, KFT, Thyroid, Hormones, Vitamin, Sugar tests, etc.

### 📊 2. Creates human-readable medical summaries
- Clean **English** summary  
- Clean **Hindi** summary  
- Triage-style doctor note (risk level / key concerns)

### 🩺 3. Analyzes symptoms (via agents)
- Low / Moderate / High risk classification  
- Symptom explanation in English + Hindi  
- When to see a doctor

### ❤️ 4. Gives personalized health tips
- Based on extracted report + AI summary  
- **Now powered by Google Gemini**  
- Lifestyle + diet + follow-up suggestions  
- Simple, safe, non-prescriptive tips in Hinglish

### 🧮 5. Web Dashboard (Streamlit)
- Upload report from browser  
- See extracted data as a clean table  
- View English/Hindi summary + tips  
- Ask questions via **“Ask with AI” chat panel** (context-aware)

### 💾 6. Stores patient history
- Per-patient **history stored on disk** (folder-based)  
- Each upload becomes one JSON record  
- Old reports can be reloaded from **History tab** → no need to re-upload

---

## 🧩 3. Multi-Agent Architecture

```text
        ┌─────────────────────┐
        │     User Upload      │
        │ (Streamlit Dashboard)│
        └──────────┬──────────┘
                   │
                   ▼
   ┌────────────────────────────────────┐
   │           Ingest Agent             │
   │  OCR → Parser → Store in Memory    │
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
    │  Personalized Tips + Reminders  │
    │  (now Gemini-powered)           │
    └─────────────────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────┐
    │     Streamlit Web Dashboard     │
    │  Summary View + Chat with AI    │
    └─────────────────────────────────┘

```

---

### 🧠 4. Key Concepts Used

✅ Multi-Agent System (Ingest, Summary, Symptom, Tips, Orchestrator)

✅ Sequential Agents (pipeline-style processing)

✅ Custom Tools (OCRTool, ParserTool)

✅ Memory (per-patient JSON / folder-based storage)

✅ Context Engineering (clean summaries, chat context)

✅ Observability (print sections in notebook, logging)

✅ Web UI with Streamlit (dashboard + chat)

✅ Google Gemini Integration

   * Health tips generation
   * Context-aware chat about the report

---

### ⚙️ 5. Project Features

✔ Upload any lab report (PDF / JPG / PNG)

✔ Automated extraction of key parameters

✔ English + Hindi medical summary

✔ Doctor-style note (triage / seriousness)

✔ Personalized health tips (Gemini + Agents)

✔ Symptom triage via agents (from notebook/orchestrator)

✔ Streamlit Dashboard UI:

   * Dark / Light mode toggle

   * Cards for Extracted Data, Summary, Tips

   * Fixed-height chat area on right

✔ Ask with AI:

   * Gemini-style interface using report context

   * Never asks user to upload again (report already in context)

✔ Patient-wise history:

   * memory/<patient_id>/record_x.json

   * History tab to browse previous reports

   * Single-click “View Full Report” to reload past data

---

### 📁 6. Project Structure

  Notebook + Web App hybrid project

    HealthBuddy/
    │
    ├── agents/
    │   ├── ingest_agent.py
    │   ├── summary_agent.py
    │   ├── chat_agent.py
    │   ├── tips_agent.py
    │   └── orchestrator.py
    │
    ├── tools/
    │   ├── ocr_tool.py
    │   └── parser_tool.py
    │
    ├── memory/
    │   ├── user1/
    │   │   ├── 1712345678.json
    │   │   └── 1712348901.json
    │   └── ... per-patient folders
    │
    ├── data/
    │   └── sample_report.pdf   (optional, for testing)
    │
    ├── streamlit_app.py        
    ├── requirements.txt
    └── README.md

---

# 🚀 7. How to Run
🟢 Option A — Run Full Dashboard (Local / Colab + Cloudflare / Streamlit Cloud)

1. Install dependencies:

       pip install -r requirements.txt
2. Run Streamlit app:
  
       streamlit run streamlit_app.py
3. Open browser at:

  * http://localhost:8501 (local)

  * Or your Cloudflare / Streamlit Cloud public URL
4. In the UI:

  * Enter Patient ID (e.g., user1)

  * Upload lab report (PDF/JPG/PNG)

  * Wait for processing

  * View:

       * Extracted Data

       * Summary (English/Hindi/Doctor Note)

       * Health Tips

       * Ask with AI chat

 * Go to Patient History tab to view past reports.

---

🟣 Option B — Run Orchestrator in Colab

1. Open HealthBuddy.ipynb in Google Colab

2. Run setup cells:

    * Install libraries

    * Create folders

    * Configure paths

3. Use the orchestrator:

       from agents.orchestrator import HealthAgentOrchestrator

       orc = HealthAgentOrchestrator()

       # Upload and parse
       orc.run("upload_report", file_path="report.pdf", patient_id="user1")

       # Generate summary
       orc.run("summary", patient_id="user1")

       # Symptom triage
       orc.run("symptoms", text="dizziness and headache")

       # Health tips
       orc.run("tips", patient_id="user1")

   ---

# 🧪 8. Sample Usage (Streamlit + Agents)
Streamlit (Web)

    streamlit run streamlit_app.py
Agents (Notebook)
         
    orc = HealthAgentOrchestrator()
    orc.run("upload_report", file_path="data/sample_report.pdf", patient_id="user1")
    orc.run("summary", patient_id="user1")
    orc.run("symptoms", text="fatigue and shortness of breath")
    orc.run("tips", patient_id="user1")

---

# 🔮 9. Future Improvements

⏳ Doctor-prescription summarizer (Rx sheet → explanation)

⏳ Multi-user cloud database (e.g., Firestore / Postgres)

⏳ Deeper wearable / Google Fit integration

⏳ More charts/visualizations (long-term trends, vitals timeline)

⏳ Role-based access (Doctor / Patient views)

---

# ⚠️ 10. Disclaimer

HealthBuddy is not a medical device.

   * It does not replace a doctor.

   * It is meant for education and awareness, not diagnosis.

   * Always consult a qualified healthcare professional for medical decisions.

---

# 👨‍💻 Author

Saifur Rahman

AI Developer | Google AI Agents Course Participant

  * Focus: AI Agents, LLMs, Healthcare AI, and Intelligent Dashboards

  * Built as a Capstone Project for Google 5-Day AI Agents Intensive

               
