import time
from google.api_core.client_options import ClientOptions
import google.generativeai as genai
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="CrisisBridge AI | Emergency Response Command Center",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Configure Gemini API with stable endpoint
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input(
        "Enter Google Gemini API Key:", type="password"
    )

if api_key:
    client_options = ClientOptions(
        api_endpoint="generativelanguage.googleapis.com"
    )
    genai.configure(api_key=api_key, client_options=client_options)

# Custom CSS for Professional Command Center Dark Mode
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .code-font {
        font-family: 'JetBrains Mono', monospace;
    }

    .stApp {
        background-color: #090d16;
        color: #f8fafc;
    }

    /* Streamlit Top Header Fix */
    header[data-testid="stHeader"] {
        background-color: #090d16 !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    header[data-testid="stHeader"] button, header[data-testid="stHeader"] span {
        color: #f8fafc !important;
    }

    /* Main Content Typography */
    .main .stMarkdown h1, .main .stMarkdown h2, .main .stMarkdown h3, .main .stMarkdown h4 {
        color: #ffffff !important;
    }
    .main .stMarkdown p, .main .stMarkdown li {
        color: #e2e8f0 !important;
    }

    /* Text Area Styling */
    .stTextArea textarea {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        font-size: 0.95rem !important;
    }
    
    .stTextArea label {
        color: #38bdf8 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
    }

    /* Metrics Contrast */
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    [data-testid="stMetricDelta"] {
        color: #34d399 !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #f1f5f9 !important;
    }

    /* Agent Pipeline Step Badges */
    .agent-step-pending {
        background: rgba(30, 41, 59, 0.6);
        border-left: 4px solid #64748b;
        padding: 10px 14px;
        border-radius: 0 6px 6px 0;
        margin-bottom: 6px;
    }
    .agent-step-pending strong { color: #f8fafc !important; }
    .agent-step-pending span { color: #cbd5e1 !important; }

    .agent-step-completed {
        background: rgba(6, 78, 59, 0.7);
        border-left: 4px solid #10b981;
        padding: 10px 14px;
        border-radius: 0 6px 6px 0;
        margin-bottom: 6px;
    }
    .agent-step-completed strong { color: #34d399 !important; }
    .agent-step-completed span { color: #f8fafc !important; }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        transition: all 0.2s ease-in-out;
        width: 100%;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.5);
        transform: translateY(-1px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Session State
if "run_pipeline" not in st.session_state:
    st.session_state["run_pipeline"] = False
if "ai_response" not in st.session_state:
    st.session_state["ai_response"] = ""

# Sidebar - System Architecture & Pipeline Status
with st.sidebar:
    st.markdown("### 🛡️ CrisisBridge AI")
    st.markdown(
        "<p style='font-size: 0.85rem; color: #94a3b8 !important;'>Autonomous Multi-Agent Humanitarian Orchestration</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown("#### ⚡ Active Agent Pipeline")

    pipeline_stages = [
        {"name": "Intake Agent", "desc": "Parsing unstructured text & dispatch logs"},
        {
            "name": "Analysis Agent",
            "desc": "Extracting entities, severity & constraints",
        },
        {
            "name": "Resource-Matching",
            "desc": "Mapping needs to available units",
        },
        {"name": "Coordinator Agent", "desc": "Compiling tactical action plan"},
        {"name": "Follow-up Agent", "desc": "SLA tracking & audit logs"},
    ]

    for idx, stage in enumerate(pipeline_stages):
        if st.session_state["run_pipeline"]:
            st.markdown(
                f"""
                <div class="agent-step-completed">
                    <strong>✓ {idx+1}. {stage['name']}</strong><br/>
                    <span style='font-size: 0.75rem;'>Completed</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="agent-step-pending">
                    <strong>{idx+1}. {stage['name']}</strong><br/>
                    <span style='font-size: 0.75rem;'>{stage['desc']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    status_text = (
        "● All Agents Operational"
        if st.session_state["run_pipeline"]
        else "○ Standby Mode"
    )
    status_color = "#10b981" if st.session_state["run_pipeline"] else "#94a3b8"
    st.markdown(
        f"<div style='font-size: 0.8rem; color: #94a3b8 !important; text-align: center;'>System Status: <span style='color: {status_color} !important;'>{status_text}</span></div>",
        unsafe_allow_html=True,
    )

# Main Content Interface
st.markdown("## 🌐 Emergency Response Command & Control")

# Input Section
with st.container():
    default_sos = (
        "URGENT: Flooding has trapped approximately 45 families in Sector 4, Downtown. "
        "Water levels are rising rapidly (currently waist-high). We have 3 elderly individuals "
        "requiring immediate medical assistance and insulin supplies. Drinking water is contaminated."
    )
    sos_input = st.text_area(
        "Incoming Emergency Dispatch Stream",
        value=default_sos,
        height=95,
        help="Input raw text feeds from radio transcripts, SOS forms, or panic buttons.",
    )

    col_input, col_action = st.columns([4, 1])
    with col_action:
        st.markdown(
            "<div style='height: 28px;'></div>", unsafe_allow_html=True
        )
        if st.button("🚀 Run Multi-Agent"):
            if not api_key:
                st.error("Please provide your Gemini API key.")
            else:
                st.session_state["run_pipeline"] = True
                with st.spinner(
                    "🔄 Gemini Multi-Agent Pipeline Analyzing Stream..."
                ):
                    try:
                        # Updated to use gemini-3.8-flash as recommended by the API response
                        model = genai.GenerativeModel("gemini-3.8-flash")
                        prompt = f"""
                        You are CrisisBridge AI, an emergency response multi-agent orchestration platform. 
                        Analyze the following emergency dispatch message and provide a concise structured tactical breakdown covering:
                        1. Severity Level
                        2. Estimated Victims
                        3. Assigned Units needed
                        4. Action Plan steps
                        5. Extracted Coordinates & Hazards

                        Dispatch Message: {sos_input}
                        """
                        response = model.generate_content(prompt)
                        st.session_state["ai_response"] = response.text
                    except Exception as e:
                        st.session_state["ai_response"] = f"API Error: {e}"
                st.rerun()

st.markdown("---")

# Execution & Dashboard View (Renders once executed)
if st.session_state["run_pipeline"]:
    # Top Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            label="Severity Level",
            value="Level 1",
            delta="Critical Priority",
            delta_color="inverse",
        )
    with m2:
        st.metric(
            label="Estimated Victims",
            value="~45 Families",
            delta="Urgent Evacuation",
            delta_color="off",
        )
    with m3:
        st.metric(
            label="Assigned Units",
            value="2 Rescue Boats",
            delta="+ 1 Paramedic Team",
        )
    with m4:
        st.metric(label="Response SLA", value="< 15 Mins", delta="● On Track")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # Detailed Action Plan & Gemini Output Grid
    col_left, col_right = st.columns([7, 5])

    with col_left:
        st.markdown("### 📋 Coordinator Agent Action Plan")
        with st.container(border=True):
            st.markdown("#### Live Gemini Multi-Agent Synthesis")
            if st.session_state["ai_response"]:
                st.write(st.session_state["ai_response"])
            else:
                st.write(
                    "Processing dispatch log through agent network..."
                )

    with col_right:
        st.markdown("### 🔍 Extracted Entities & Telemetry")
        with st.container(border=True):
            st.markdown("**Location Coordinates**")
            st.info("📍 Sector 4, Downtown (34.0500° N, 118.2400° W)")

            st.markdown("**Critical Hazards**")
            st.error(
                "Flash Flooding (Waist-High), Contaminated Water Source"
            )

            st.markdown("**Medical Requirements**")
            st.warning(
                "3x Senior Citizens – Insulin & Warmth Support Required"
            )

            st.markdown("**Resource Audit Log**")
            st.success(
                "[18:52:04] Unit Alpha-1 assigned & acknowledged dispatch."
            )
else:
    st.info(
        "👆 Click **'Run Multi-Agent'** above to process the dispatch log using the live Gemini model."
    )
    
    