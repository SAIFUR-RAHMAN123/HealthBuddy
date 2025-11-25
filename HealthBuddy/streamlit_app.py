import streamlit as st
import json, os, time
import pandas as pd
from datetime import datetime

# Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Agents
from agents.ingest_agent import IngestAgent
from agents.summary_agent import SummaryAgent
from agents.chat_agent import ChatAgent

#############################################
# 0. SESSION STATE INIT
#############################################
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

session_defaults = {
    "processing_complete": False,
    "extracted_data": None,
    "summary_data": None,
    "health_tips": None,
    "chat_history": [],
    "detected_name": None,
    "last_file": None,
    "gemini_configured": False,
    "current_view": "Summarizer Dashboard"  # Navigation control variable
}
for k, v in session_defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

theme = st.session_state["theme"]

#############################################
# 1. PAGE CONFIG
#############################################
st.set_page_config(
    page_title="AI Medical Report Summarizer",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

#############################################
# 2. THEME COLORS
#############################################
if theme == "light":
    APP_BG = "linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%)"
    VIEW_BG = "linear-gradient(to right top, #fff1eb, #ace0f9)"
    CARD_BG = "rgba(255,255,255,0.96)"
    TEXT_COLOR = "#111"
    SIDEBAR_BG = "rgba(255,255,255,0.35)"
    CHAT_USER_BG = "#e3f2fd"
    CHAT_ASSISTANT_BG = "#f9fafb"
else:
    APP_BG = "linear-gradient(135deg, #020617 0%, #0f172a 100%)"
    VIEW_BG = "linear-gradient(to right top, #020617, #0f172a)"
    CARD_BG = "rgba(15,23,42,0.96)"
    TEXT_COLOR = "#f9fafb"
    SIDEBAR_BG = "rgba(15,23,42,0.85)"
    CHAT_USER_BG = "#0ea5e9"
    CHAT_ASSISTANT_BG = "#1f2937"

#############################################
# 3. GLOBAL CSS
#############################################
st.markdown(f"""
    <style>
    header {{visibility:hidden;}}
    footer {{visibility:hidden;}}

    .stApp {{
        background:{APP_BG};
    }}
    [data-testid="stAppViewContainer"] {{
        background-image:{VIEW_BG};
    }}

    .css-card {{
        padding:20px;
        border-radius:18px;
        background:{CARD_BG};
        border:1px solid rgba(255,255,255,0.1);
        box-shadow:0 6px 20px rgba(0,0,0,0.3);
        margin-bottom:14px;
    }}

    [data-testid="stSidebar"] {{
        background:{SIDEBAR_BG};
        backdrop-filter: blur(20px);
        border-right:1px solid rgba(255,255,255,0.25);
    }}

    .chat-bubble {{
        padding:8px 12px;
        border-radius:14px;
        margin-bottom:6px;
        max-width:100%;
        line-height:1.4;
        word-wrap:break-word;
    }}
    .chat-bubble.user {{
        background:{CHAT_USER_BG};
        color:#000;
    }}
    .chat-bubble.assistant {{
        background:{CHAT_ASSISTANT_BG};
        color:{TEXT_COLOR};
    }}

    .tips-card {{
        background:radial-gradient(circle at top left,#4f46e5,#7c3aed,#db2777,#0f172a);
        color:white;
        padding:22px;
        border-radius:20px;
    }}
    
    .history-item {{
        background: {CARD_BG};
        border: 1px solid rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

#############################################
# 4. HELPERS
#############################################
def flatten_json_to_df(data):
    if not data:
        return pd.DataFrame()
    out = {}
    for k, v in data.items():
        if isinstance(v, (str, int, float)):
            out[k] = v
        elif isinstance(v, dict) and "value" in v:
            out[k] = f"{v['value']} {v.get('unit','')}"
        else:
            out[k] = str(v)
    return pd.DataFrame(out.items(), columns=["Parameter", "Result"]) if out else pd.DataFrame()


def configure_gemini_once():
    """Load Google AI Studio API key"""
    if not GEMINI_AVAILABLE:
        return
    if not st.session_state["gemini_configured"]:
        key = os.getenv("GEMINI_API_KEY")
        if key:
            genai.configure(api_key=key)
            st.session_state["gemini_configured"] = True

#############################################
# 5. GEMINI HEALTH TIPS 
#############################################
def generate_health_tips_with_gemini(extracted, summary):
    if not GEMINI_AVAILABLE:
        return ["Gemini SDK install nahi hai."]

    configure_gemini_once()

    prompt = f"""
    Based on the following blood/lab report:
    LAB DATA: {json.dumps(extracted, ensure_ascii=False)}
    SUMMARY: {json.dumps(summary, ensure_ascii=False)}

    Generate 5–8 helpful, SAFE, Hinglish health tips.
    Format MUST be bullet list starting with "-".
    """

    try:
        # Step 1: Auto-detect available models
        available_model = None
        try:
            for m in genai.list_models():
                if 'generateContent' in getattr(m, "supported_generation_methods", []):
                    # Prefer flash or pro
                    if 'flash' in m.name:
                        available_model = m.name
                        break
                    if 'pro' in m.name and not available_model:
                        available_model = m.name
        except Exception:
            pass  # ignore list_models issues

        # Fallback list agar auto-detect fail ho
        candidates = [available_model] if available_model else []
        candidates += ["gemini-1.5-flash", "gemini-1.5-flash-latest", "gemini-pro", "gemini-1.0-pro"]
        candidates = list(dict.fromkeys([c for c in candidates if c]))  # unique, remove None

        last_error = ""

        for model_name in candidates:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                if response and getattr(response, "text", None):
                    text = response.text.strip()
                    tips = []
                    for ln in text.splitlines():
                        if ln.startswith("-") or ln.startswith("•"):
                            tips.append(ln.lstrip("-• ").strip())
                    return tips or [text]
            except Exception as e:
                last_error = str(e)
                continue

        return [f"Tips generate nahi ho paye. Last Error: {last_error}"]

    except Exception as e:
        return [f"Critical Gemini Error: {e}"]

#############################################
# Sidebar 
#############################################
with st.sidebar:
    st.markdown("### 🩺 HealthBuddy AI")

    dark = st.toggle("🌗 Dark Mode", value=(theme == "dark"))
    st.session_state["theme"] = "dark" if dark else "light"

    patient_id = st.text_input("Patient ID", "user1")

    # Navigation controlled via state
    options = ["Summarizer Dashboard", "Advanced History"]
    try:
        curr_idx = options.index(st.session_state["current_view"])
    except ValueError:
        curr_idx = 0

    selected_nav = st.radio("Menu", options, index=curr_idx)

    if selected_nav != st.session_state["current_view"]:
        st.session_state["current_view"] = selected_nav
        st.rerun()

    nav = st.session_state["current_view"]

#############################################
# MAIN DASHBOARD
#############################################
ingest_agent = IngestAgent()
summary_agent = SummaryAgent()
chat_agent = ChatAgent()

if nav == "Summarizer Dashboard":

    st.markdown('<h1 class="gradient-text">AI Medical Report Summarizer</h1>', unsafe_allow_html=True)
    st.caption("Upload report → Extract → Summarize → Health Tips")

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        uploaded = st.file_uploader("Upload PDF/Image", type=["pdf", "png", "jpg", "jpeg"])

    # New file processing
    if uploaded and st.session_state.last_file != uploaded.name:
        path = f"data/{uploaded.name}"
        os.makedirs("data", exist_ok=True)

        pb = st.progress(0)
        for p in range(0, 101, 20):
            time.sleep(0.1)
            pb.progress(p)

        with open(path, "wb") as f:
            f.write(uploaded.read())
        st.session_state.last_file = uploaded.name

        with st.status("Processing report...", expanded=True):
            raw = ingest_agent.run(path, patient_id)
            summary = summary_agent.run(patient_id)
            tips = generate_health_tips_with_gemini(raw, summary)

            st.session_state.extracted_data = raw
            st.session_state.summary_data = summary
            st.session_state.health_tips = tips
            st.session_state.processing_complete = True

            # ==========================
            # SAVE HISTORY TO PATIENT FOLDER (CORRECT PLACE)
            # ==========================
            patient_folder = f"memory/{patient_id}"
            os.makedirs(patient_folder, exist_ok=True)

            record = {
                "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "extracted_data": raw,
                "summary": summary,
                "health_tips": tips
            }

            filename = f"{patient_folder}/{int(time.time())}.json"
            with open(filename, "w") as fp:
                json.dump(record, fp, indent=2)

        st.rerun()

    # Display Dashboard if data exists
    if st.session_state.processing_complete and st.session_state.extracted_data:

        left, right = st.columns([2, 1])

        ###################################
        # LEFT SIDE
        ###################################
        with left:

            a, b = st.columns(2)

            # Extract
            with a:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                st.subheader("📊 Extracted Data")
                df = flatten_json_to_df(st.session_state.extracted_data)
                st.dataframe(df, hide_index=True, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Summary
            with b:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                st.subheader("📋 Medical Summary")
                s = st.session_state.summary_data
                t = st.tabs(["English", "Hindi", "Doctor"])
                t[0].markdown(s.get("english_summary", "N/A"))
                t[1].markdown(s.get("hindi_summary", "N/A"))
                t[2].markdown(s.get("doctor_note", "N/A"))
                st.markdown('</div>', unsafe_allow_html=True)

            # Health Tips
            st.markdown('<div class="tips-card">', unsafe_allow_html=True)
            st.markdown("<h3>💡 Health Tips (Report-based)</h3>", unsafe_allow_html=True)

            tips = st.session_state.health_tips or []
            if tips and isinstance(tips, list):
                st.markdown("<ul>", unsafe_allow_html=True)
                for tip in tips:
                    st.markdown(f"<li>{tip}</li>", unsafe_allow_html=True)
                st.markdown("</ul>", unsafe_allow_html=True)
            else:
                st.write(str(tips))

            st.markdown(
                "<p style='font-size:0.8rem;opacity:0.7;'>⚠️ Ye tips general guidance ke liye hain.</p>",
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

        ###################################
        # RIGHT CHAT 
        ###################################
        with right:
            st.markdown('<div class="css-card">', unsafe_allow_html=True)
            st.subheader("💬 Ask with AI")

            chat_box = st.container(height=500)
            with chat_box:
                for m in st.session_state.chat_history:
                    cls = "user" if m["role"] == "user" else "assistant"
                    st.markdown(f"<div class='chat-bubble {cls}'>{m['content']}</div>", unsafe_allow_html=True)

            msg = st.chat_input("Ask anything...")
            if msg:
                st.session_state.chat_history.append({"role": "user", "content": msg})

                ctx = {
                    "report": st.session_state.extracted_data,
                    "summary": st.session_state.summary_data,
                    "tips": st.session_state.health_tips
                }

                final_prompt = (
                    f"User Query: {msg}\n\n"
                    f"Use this report context:\n{json.dumps(ctx, ensure_ascii=False)}\n\n"
                    f"Never ask user to upload report again."
                )

                ans = chat_agent.run(patient_id, final_prompt)
                st.session_state.chat_history.append({"role": "assistant", "content": ans})
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("👆 Please upload a medical report to start.")

#############################################
# HISTORY PAGE (Patient-based Folder Storage)
#############################################
else:
    st.markdown('<h2 class="gradient-text">📂 Patient History</h2>', unsafe_allow_html=True)

    # Patient-specific folder
    patient_folder = f"memory/{patient_id}"
    os.makedirs(patient_folder, exist_ok=True)

    # List JSON files
    history_files = sorted(
        [f for f in os.listdir(patient_folder) if f.endswith(".json")],
        reverse=True
    )

    if not history_files:
        st.warning("No history found for this patient.")
    else:
        for i, file in enumerate(history_files):
            fullpath = os.path.join(patient_folder, file)

            try:
                entry = json.load(open(fullpath))

                ts = entry.get("timestamp", file.replace(".json", ""))
                extracted = entry.get("extracted_data", {})
                summary = entry.get("summary", {})
                tips = entry.get("health_tips", [])

                eng_summary = summary.get("english_summary", "No summary available")
                preview = eng_summary[:150] + "..."

                # Display summary card
                st.markdown(f"""
                <div class="history-item" style="
                    background: rgba(255,255,255,0.08);
                    padding: 15px; 
                    margin-bottom: 12px;
                    border-radius: 12px;
                    border: 1px solid rgba(255,255,255,0.15);">
                    
                    <h4>📅 {ts}</h4>
                    <p style='opacity:0.85'>{preview}</p>
                </div>
                """, unsafe_allow_html=True)

                # View button
                if st.button(f"🔎 View Full Report ({ts})", key=f"history_{i}"):

                    # Load saved data into current session
                    st.session_state.extracted_data = extracted
                    st.session_state.summary_data = summary

                    # Auto-generate tips if missing
                    if not tips:
                        with st.spinner("Generating health tips..."):
                            tips = generate_health_tips_with_gemini(extracted, summary)

                    st.session_state.health_tips = tips
                    st.session_state.processing_complete = True

                    # Reset chat for new report
                    st.session_state.chat_history = []

                    # Redirect to Dashboard
                    st.session_state["current_view"] = "Summarizer Dashboard"
                    st.rerun()

            except Exception as e:
                st.error(f"Error reading history file {file}: {e}")
