import streamlit as st
import joblib
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Fraud Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { font-family: 'Inter', sans-serif !important; }

/* ── Dark background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1100px; margin: auto; }

/* ── Hero banner ── */
.hero {
    text-align: center;
    padding: 3rem 2rem 2rem;
    margin-bottom: 2rem;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.5);
    color: #a5b4fc;
    padding: 0.3rem 1rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.6rem;
    line-height: 1.1;
}
.hero p {
    color: #94a3b8;
    font-size: 1.05rem;
    max-width: 540px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Glass cards ── */
.glass-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.card-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Streamlit input overrides ── */
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s;
}
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.15) !important;
}
label, .stSelectbox label, .stNumberInput label {
    color: #cbd5e1 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ── Slider ── */
div[data-testid="stSlider"] > div > div > div {
    background: linear-gradient(90deg, #a78bfa, #60a5fa) !important;
}
div[data-testid="stSlider"] p { color: #94a3b8 !important; font-size: 0.82rem !important; }

/* ── Submit button ── */
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(124,58,237,0.55) !important;
}

/* ── Result boxes ── */
.result-fraud {
    background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(185,28,28,0.1));
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    text-align: center;
    animation: pulse-red 2s infinite;
}
.result-safe {
    background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(5,150,105,0.1));
    border: 1px solid rgba(16,185,129,0.4);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    text-align: center;
    animation: pulse-green 2s infinite;
}
@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); }
    50%       { box-shadow: 0 0 0 8px rgba(239,68,68,0.08); }
}
@keyframes pulse-green {
    0%, 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
    50%       { box-shadow: 0 0 0 8px rgba(16,185,129,0.08); }
}
.result-emoji { font-size: 3.5rem; margin-bottom: 0.5rem; }
.result-fraud h2  { color: #f87171; font-size: 1.6rem; font-weight: 800; margin: 0; }
.result-safe h2   { color: #34d399; font-size: 1.6rem; font-weight: 800; margin: 0; }
.result-sub { color: #94a3b8; font-size: 0.9rem; margin-top: 0.4rem; }

/* ── Metric tiles ── */
.metric-row { display: flex; gap: 1rem; margin-top: 1.5rem; flex-wrap: wrap; }
.metric-tile {
    flex: 1; min-width: 120px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-tile .val { font-size: 1.5rem; font-weight: 800; color: #f1f5f9; }
.metric-tile .lbl { font-size: 0.72rem; color: #64748b; letter-spacing: 1px; text-transform: uppercase; margin-top: 0.2rem; }

/* ── Gauge bar ── */
.gauge-wrap { margin-top: 1.2rem; }
.gauge-track {
    background: rgba(255,255,255,0.08);
    border-radius: 999px;
    height: 12px;
    overflow: hidden;
    margin-top: 0.5rem;
}
.gauge-fill-safe  { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #34d399, #10b981); transition: width 0.8s cubic-bezier(.4,0,.2,1); }
.gauge-fill-fraud { height: 100%; border-radius: 999px; background: linear-gradient(90deg, #f87171, #ef4444); transition: width 0.8s cubic-bezier(.4,0,.2,1); }
.gauge-labels { display: flex; justify-content: space-between; color: #475569; font-size: 0.72rem; margin-top: 0.3rem; }

/* ── Expander ── */
details summary { color: #a78bfa !important; font-size: 0.85rem !important; font-weight: 600 !important; }
div[data-testid="stExpander"] { background: rgba(255,255,255,0.03) !important; border-color: rgba(255,255,255,0.08) !important; border-radius: 12px !important; }

/* ── Dataframe ── */
div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.08) !important; }

/* ── Footer ── */
.footer { text-align: center; color: #334155; font-size: 0.78rem; margin-top: 3rem; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    model    = joblib.load("fraud_detection_model.pkl")
    features = joblib.load("fraud_detection_features.pkl")
    return model, features

model, feature_names = load_model()
TRANSACTION_TYPES = ["CASH_IN", "CASH_OUT", "DEBIT", "PAYMENT", "TRANSFER"]

TYPE_ICONS = {
    "CASH_IN": "💰", "CASH_OUT": "💸",
    "DEBIT": "🏧", "PAYMENT": "💳", "TRANSFER": "🔁"
}

st.markdown("""
<div class="hero">
    <div class="hero-badge">🛡️ AI-Powered Detection</div>
    <h1>Fraud Shield</h1>
    <p>Real-time online payment fraud detection powered by machine learning. Enter transaction details to get an instant risk assessment.</p>
</div>
""", unsafe_allow_html=True)

with st.form("fraud_form"):
    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.markdown('<div class="card-title">📋 Transaction Details</div>', unsafe_allow_html=True)

        tx_type = st.selectbox(
            "Transaction Type",
            options=TRANSACTION_TYPES,
            format_func=lambda x: f"{TYPE_ICONS[x]}  {x.replace('_', ' ').title()}"
        )
        amount = st.number_input(
            "Transaction Amount (₹)",
            min_value=0.0, value=15000.0, step=500.0, format="%.2f"
        )
        step = st.number_input(
            "Simulation Step (1 step = 1 hour)",
            min_value=1, max_value=744, value=1,
        )

    with col_right:
        st.markdown('<div class="card-title">🏦 Account Balances</div>', unsafe_allow_html=True)

        oldbalanceOrg = st.number_input(
            "Sender Balance — Before Transaction (₹)",
            min_value=0.0, value=50000.0, step=1000.0, format="%.2f"
        )
        newbalanceOrig = st.number_input(
            "Sender Balance — After Transaction (₹)",
            min_value=0.0, value=35000.0, step=1000.0, format="%.2f"
        )
        oldbalanceDest = st.number_input(
            "Receiver Balance — Before Transaction (₹)",
            min_value=0.0, value=20000.0, step=1000.0, format="%.2f"
        )
        newbalanceDest = st.number_input(
            "Receiver Balance — After Transaction (₹)",
            min_value=0.0, value=35000.0, step=1000.0, format="%.2f"
        )

    st.markdown("---")
    st.markdown('<div class="card-title">⚙️ Detection Sensitivity</div>', unsafe_allow_html=True)
    threshold = st.slider(
        "Risk Threshold — lower value = more sensitive (catches more fraud, may flag some legit transactions)",
        min_value=0.1, max_value=0.9, value=0.5, step=0.05,
        format="%.2f"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("⚡  Analyze Transaction", use_container_width=True)

if submitted:
    input_dict = {
        "step": step,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest,
        "type_CASH_IN":  1 if tx_type == "CASH_IN"  else 0,
        "type_CASH_OUT": 1 if tx_type == "CASH_OUT" else 0,
        "type_DEBIT":    1 if tx_type == "DEBIT"    else 0,
        "type_PAYMENT":  1 if tx_type == "PAYMENT"  else 0,
        "type_TRANSFER": 1 if tx_type == "TRANSFER" else 0,
    }
    input_df   = pd.DataFrame([input_dict])[feature_names]
    fraud_prob = float(model.predict_proba(input_df)[0, 1])
    is_fraud   = fraud_prob >= threshold
    safe_prob  = 1 - fraud_prob

    st.markdown("<br>", unsafe_allow_html=True)

    if is_fraud:
        st.markdown(f"""
        <div class="result-fraud">
            <div class="result-emoji">🚨</div>
            <h2>FRAUDULENT TRANSACTION</h2>
            <p class="result-sub">This transaction has been flagged as high-risk. Immediate review recommended.</p>
        </div>
        """, unsafe_allow_html=True)
        gauge_class = "gauge-fill-fraud"
        risk_color  = "#f87171"
    else:
        st.markdown(f"""
        <div class="result-safe">
            <div class="result-emoji">✅</div>
            <h2>LEGITIMATE TRANSACTION</h2>
            <p class="result-sub">This transaction appears safe based on the current risk threshold.</p>
        </div>
        """, unsafe_allow_html=True)
        gauge_class = "gauge-fill-safe"
        risk_color  = "#34d399"

    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-tile">
            <div class="val" style="color:{risk_color}">{fraud_prob:.1%}</div>
            <div class="lbl">Fraud Risk</div>
        </div>
        <div class="metric-tile">
            <div class="val">{safe_prob:.1%}</div>
            <div class="lbl">Safety Score</div>
        </div>
        <div class="metric-tile">
            <div class="val">{"🔴 HIGH" if fraud_prob > 0.7 else "🟡 MEDIUM" if fraud_prob > 0.3 else "🟢 LOW"}</div>
            <div class="lbl">Risk Level</div>
        </div>
        <div class="metric-tile">
            <div class="val">{threshold:.0%}</div>
            <div class="lbl">Threshold</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="gauge-wrap">
        <span style="color:#94a3b8; font-size:0.82rem; font-weight:600;">FRAUD PROBABILITY GAUGE</span>
        <div class="gauge-track">
            <div class="{gauge_class}" style="width:{fraud_prob*100:.1f}%"></div>
        </div>
        <div class="gauge-labels"><span>0%</span><span>Threshold: {threshold:.0%}</span><span>100%</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🔍 View Raw Feature Input"):
        st.dataframe(
            input_df.T.rename(columns={0: "Value"}).style.format("{:.4f}"),
            use_container_width=True
        )

st.markdown("""
<div class="footer">
    Fraud Shield &nbsp;·&nbsp; Trained on PaySim Synthetic Dataset &nbsp;·&nbsp; Built with Streamlit 🎈
</div>
""", unsafe_allow_html=True)
