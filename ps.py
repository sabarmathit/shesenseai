import streamlit as st
import pandas as pd
import pydeck as pdk
import random
import datetime as dt
import json
import numpy as np
import threading
from pathlib import Path
from PIL import Image

try:
    import pyttsx3
    TTS_AVAILABLE = True
except Exception:
    TTS_AVAILABLE = False

try:
    from streamlit_autorefresh import st_autorefresh
    AUTO_REFRESH_AVAILABLE = True
except Exception:
    AUTO_REFRESH_AVAILABLE = False

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="SheSense SafeRoute AI+",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# GLOBAL CSS — Dark Luxury Theme
# -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700&display=swap');

:root {
    --primary: #e91e8c;
    --primary-dark: #b5136a;
    --accent: #00f0ff;
    --accent2: #ff6b35;
    --bg-dark: #050a14;
    --bg-card: #0d1623;
    --bg-card2: #111c2e;
    --text: #e8f0fe;
    --text-muted: #8898aa;
    --danger: #ff3b5c;
    --success: #00e676;
    --warning: #ffab00;
    --border: rgba(0,240,255,0.15);
    --glow: 0 0 20px rgba(233,30,140,0.4);
    --glow-accent: 0 0 20px rgba(0,240,255,0.3);
}

html, body, [class*="css"] {
    font-family: 'Exo 2', sans-serif !important;
    background-color: var(--bg-dark) !important;
    color: var(--text) !important;
}

#MainMenu, footer, header { visibility: hidden; }

.main .block-container {
    padding: 1rem 2rem 2rem 2rem !important;
    max-width: 1400px !important;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f1e 0%, #050a14 100%) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] .stRadio label {
    color: var(--text) !important;
    font-family: 'Exo 2', sans-serif !important;
}

h1 {
    font-family: 'Orbitron', monospace !important;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-size: 2.2rem !important;
    font-weight: 900 !important;
    text-shadow: none !important;
    letter-spacing: 2px !important;
    margin-bottom: 0 !important;
}

h2, h3 {
    font-family: 'Orbitron', monospace !important;
    color: var(--accent) !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 0.4rem !important;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div {
    background: var(--bg-card2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'Exo 2', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: var(--glow) !important;
}
.stTextInput label, .stNumberInput label, .stTextArea label,
.stSelectbox label, .stCheckbox label {
    color: var(--text-muted) !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--primary-dark), var(--primary)) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Exo 2', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 0.5rem 1.5rem !important;
    text-transform: uppercase !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(233,30,140,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--glow) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}
[data-testid="metric-container"] label {
    color: var(--text-muted) !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-family: 'Orbitron', monospace !important;
}

.stAlert {
    border-radius: 10px !important;
    border-left: 4px solid !important;
    font-family: 'Exo 2', sans-serif !important;
}

.stCheckbox > label > span { color: var(--text) !important; }

.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    color: var(--accent) !important;
    font-family: 'Exo 2', sans-serif !important;
    border-radius: 8px !important;
}

.stRadio > div { gap: 0.3rem !important; }
.stRadio > div > label {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 0.5rem 0.75rem !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}
.stRadio > div > label:hover {
    border-color: var(--primary) !important;
    background: rgba(233,30,140,0.08) !important;
}

.she-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}
.she-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
}

.emergency-pulse {
    animation: pulse-red 1s infinite;
    border-radius: 12px;
}
@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 0 0 rgba(255,59,92,0.7); }
    50% { box-shadow: 0 0 0 20px rgba(255,59,92,0); }
}

.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.badge-safe { background: rgba(0,230,118,0.15); color: var(--success); border: 1px solid rgba(0,230,118,0.3); }
.badge-warn { background: rgba(255,171,0,0.15); color: var(--warning); border: 1px solid rgba(255,171,0,0.3); }
.badge-danger { background: rgba(255,59,92,0.15); color: var(--danger); border: 1px solid rgba(255,59,92,0.3); }

.login-hero {
    text-align: center;
    padding: 2rem 0 1.5rem 0;
}
.login-hero .hero-icon {
    font-size: 4rem;
    margin-bottom: 0.5rem;
    display: block;
    filter: drop-shadow(0 0 20px rgba(233,30,140,0.6));
}
.login-hero h1 {
    font-family: 'Orbitron', monospace !important;
    font-size: 2.5rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #e91e8c, #00f0ff) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}
.login-hero p {
    color: var(--text-muted) !important;
    font-size: 1rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

.info-box {
    background: rgba(0,240,255,0.06);
    border: 1px solid rgba(0,240,255,0.2);
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 0.75rem;
}
.info-box .info-label {
    color: var(--accent);
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 700;
    margin-bottom: 0.2rem;
}
.info-box .info-value {
    color: var(--text);
    font-size: 1rem;
    font-weight: 500;
}

.voice-panel {
    background: linear-gradient(135deg, rgba(0,240,255,0.04), rgba(233,30,140,0.04));
    border: 1px solid rgba(0,240,255,0.15);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-top: 1rem;
}
.voice-indicator {
    width: 12px; height: 12px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
    vertical-align: middle;
}
.voice-indicator.active {
    background: var(--success);
    animation: blink 1s infinite;
}
.voice-indicator.inactive { background: var(--text-muted); }
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.alert-notification {
    background: linear-gradient(135deg, rgba(255,59,92,0.15), rgba(255,59,92,0.05));
    border: 1px solid rgba(255,59,92,0.4);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    animation: pulse-red 2s infinite;
}
.alert-notification .alert-title {
    color: var(--danger);
    font-family: 'Orbitron', monospace;
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 0.4rem;
}
.alert-notification .alert-body { color: var(--text); font-size: 0.9rem; }

.module-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.5rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--border);
}
.module-icon { font-size: 1.8rem; filter: drop-shadow(0 0 8px currentColor); }

.severity-bar {
    height: 6px;
    border-radius: 3px;
    background: var(--bg-card2);
    overflow: hidden;
    margin: 0.5rem 0;
}
.severity-bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.5s ease;
}

.sidebar-user {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 1rem;
}
.sidebar-user .user-name { font-weight: 700; color: var(--accent); font-size: 0.95rem; }
.sidebar-user .user-status { font-size: 0.75rem; color: var(--text-muted); margin-top: 0.2rem; }

.she-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.5rem 0;
}

.step-indicator { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; align-items: center; }
.step-dot {
    width: 30px; height: 30px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem; font-weight: 700;
    border: 2px solid var(--border);
    color: var(--text-muted);
}
.step-dot.active { border-color: var(--primary); background: rgba(233,30,140,0.15); color: var(--primary); }
.step-dot.done { border-color: var(--success); background: rgba(0,230,118,0.15); color: var(--success); }
.step-line { flex: 1; height: 1px; background: var(--border); }

.police-theme h3 { color: #4fc3f7 !important; }
.hospital-theme h3 { color: #ef5350 !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-dark); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

.map-container { border: 1px solid var(--border); border-radius: 12px; overflow: hidden; margin-top: 0.5rem; }

.contact-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.contact-avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.9rem; color: white;
    flex-shrink: 0;
}

.role-card {
    background: var(--bg-card);
    border: 2px solid var(--border);
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
}
.role-card:hover, .role-card.selected {
    border-color: var(--primary);
    background: rgba(233,30,140,0.08);
    box-shadow: var(--glow);
}
.role-card .role-icon { font-size: 2.5rem; margin-bottom: 0.5rem; display: block; }
.role-card .role-name { font-family: 'Orbitron', monospace; font-weight: 700; font-size: 0.9rem; color: var(--text); letter-spacing: 1px; }
.role-card .role-desc { font-size: 0.75rem; color: var(--text-muted); margin-top: 0.3rem; }

.otp-section {
    background: rgba(0,240,255,0.04);
    border: 1px dashed rgba(0,240,255,0.25);
    border-radius: 10px;
    padding: 1rem;
    margin: 0.75rem 0;
}

.eta-card {
    background: linear-gradient(135deg, rgba(255,59,92,0.1), rgba(255,107,53,0.05));
    border: 1px solid rgba(255,59,92,0.3);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.eta-time { font-family: 'Orbitron', monospace; font-size: 2rem; color: var(--danger); font-weight: 900; }
.eta-label { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; }

/* Route safety color bands */
.route-safe { border-left: 4px solid #00e676 !important; }
.route-warn  { border-left: 4px solid #ffab00 !important; }
.route-risky { border-left: 4px solid #ff3b5c !important; }

/* Navigation direction card */
.nav-direction {
    background: linear-gradient(135deg, rgba(0,240,255,0.08), rgba(0,240,255,0.02));
    border: 1px solid rgba(0,240,255,0.3);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.nav-arrow { font-size: 2rem; min-width: 2.5rem; text-align: center; }
.nav-text { flex: 1; }
.nav-dist { color: #8898aa; font-size: 0.78rem; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# DATA STORAGE
# -------------------------
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
DB_FILE = DATA_DIR / "shesense_db.json"
INCIDENT_MEDIA_DIR = DATA_DIR / "incident_media"
INCIDENT_MEDIA_DIR.mkdir(exist_ok=True)


def load_db():
    if DB_FILE.exists():
        try:
            return json.loads(DB_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"users": [], "police_users": [], "hospital_users": [], "alerts": [], "incidents": [], "route_logs": []}


def save_db(db):
    DB_FILE.write_text(json.dumps(db, indent=2), encoding="utf-8")


DB = load_db()

# -------------------------
# SESSION DEFAULTS
# -------------------------
DEFAULTS = {
    "logged_in": False,
    "user_role": "user",
    "auth_mode": "login",
    "otp_sent": False,
    "generated_otp": "",
    "otp_verified": False,
    "mobile_number": "",
    "user_name": "",
    "distress_word": "",
    "contact_1_name": "", "contact_1_number": "",
    "contact_2_name": "", "contact_2_number": "",
    "contact_3_name": "", "contact_3_number": "",
    "location_enabled": False,
    "latitude": 11.0168,
    "longitude": 76.9558,
    "destination_name": "",
    "destination_lat": 11.0268,
    "destination_lon": 76.9658,
    "route_safety": "Unknown",
    "route_reason": "",
    "selected_route": "Not selected",
    "network_status": "Online",
    "emergency_status": "Normal",
    "alarm_active": False,
    "recognized_speech": "",
    "listening_status": "Not Listening",
    "fearful_voice_detected": False,
    "queued_alerts": [],
    "last_alert_time": "",
    "incident_report": "",
    "incident_media_files": [],
    "pregnant_mode": False,
    "pregnant_severity": "Normal",
    "pregnant_patient_data": {},
    "police_station_name": "Coimbatore Central Police Station",
    "police_station_branch": "Law & Order Division",
    "police_station_address": "Town Hall Road, Coimbatore",
    "hospital_name": "City Emergency Hospital",
    "hospital_branch": "Emergency & Trauma Care",
    "hospital_address": "Avinashi Road, Coimbatore",
    "light_status": "Not checked",
    "voice_last_message": "",
    "police_badge_id": "",
    "police_station": "",
    "police_division": "",
    "hospital_reg_name": "",
    "hospital_reg_dept": "",
    "hospital_reg_id": "",
    "selected_role": "User",
    "navigation_active": False,
    "current_step_index": 0,
    "camera_light_result": "",
    "neighbor_alarm_active": False,
    # Hospital/Ambulance pregnancy patient details
    "amb_patient_name": "",
    "amb_patient_age": 0,
    "amb_due_date": "",
    "amb_blood_group": "",
    "amb_complications": "",
    "amb_route_checked": False,
    "amb_route_safety": "Unknown",
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -------------------------
# AUTO REFRESH
# -------------------------
if AUTO_REFRESH_AVAILABLE:
    st_autorefresh(interval=4000, key="refresh_key")


# -------------------------
# HELPERS
# -------------------------
def now_str():
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def speak_async(message: str):
    st.session_state.voice_last_message = message
    if not TTS_AVAILABLE:
        return
    def _speak():
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 160)
            engine.say(message)
            engine.runAndWait()
        except Exception:
            pass
    threading.Thread(target=_speak, daemon=True).start()


def generate_otp():
    return str(random.randint(100000, 999999))


def validate_mobile(number: str):
    digits = "".join(ch for ch in number if ch.isdigit())
    return len(digits) >= 10


def enable_live_location():
    st.session_state.location_enabled = True
    st.session_state.latitude = 11.0168
    st.session_state.longitude = 76.9558
    speak_async("Current location enabled successfully")


def get_google_maps_url(lat, lon):
    return f"https://www.google.com/maps?q={lat},{lon}"


def get_google_maps_directions_url(src_lat, src_lon, dst_lat, dst_lon):
    return f"https://www.google.com/maps/dir/{src_lat},{src_lon}/{dst_lat},{dst_lon}"


def get_google_maps_embed_url(src_lat, src_lon, dst_lat, dst_lon, mode="driving"):
    return (f"https://www.google.com/maps/embed/v1/directions"
            f"?key=AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY"
            f"&origin={src_lat},{src_lon}&destination={dst_lat},{dst_lon}&mode={mode}")


def classify_route(night, low_light, isolated, crowd, near_hospital, near_police):
    score = 0
    if night: score += 2
    if low_light: score += 2
    if isolated: score += 3
    if crowd == "Low": score += 2
    elif crowd == "Medium": score += 1
    else: score -= 1
    if near_hospital: score -= 1
    if near_police: score -= 1
    if score <= 1:
        return "High Safe", "Recommended route avoids risky zones and has strong public and emergency access."
    elif score <= 4:
        return "Low Safe", "Route is usable but some caution is required. Stay alert."
    return "Risky Area", "This route has multiple risk factors. Consider an alternate route."


def classify_safety(night, low_light, isolated, distress_text):
    score = 0
    if night: score += 2
    if low_light: score += 2
    if isolated: score += 3
    if distress_text.strip(): score += 3
    if score <= 2: return "High Safe"
    elif score <= 5: return "Low Safe"
    elif score <= 7: return "Risky Area"
    return "Critical Emergency"


def pregnant_severity_from_symptom(symptom):
    if symptom == "Critical": return "Critical"
    if symptom in ["Pain", "Bleeding", "Dizziness"]: return "High Risk"
    return "Normal"


def persist_user():
    user = {
        "mobile_number": st.session_state.mobile_number,
        "user_name": st.session_state.user_name,
        "distress_word": st.session_state.distress_word,
        "contacts": [
            {"name": st.session_state.contact_1_name, "phone": st.session_state.contact_1_number},
            {"name": st.session_state.contact_2_name, "phone": st.session_state.contact_2_number},
            {"name": st.session_state.contact_3_name, "phone": st.session_state.contact_3_number},
        ],
        "saved_at": now_str()
    }
    DB["users"] = [u for u in DB["users"] if u.get("mobile_number") != st.session_state.mobile_number]
    DB["users"].append(user)
    save_db(DB)


def build_alert(recipient_type, recipient_name):
    return {
        "recipient_type": recipient_type,
        "recipient_name": recipient_name,
        "mobile_number": st.session_state.mobile_number,
        "location": {"lat": st.session_state.latitude, "lon": st.session_state.longitude},
        "time": now_str(),
        "distress_word": st.session_state.distress_word,
        "risk_level": st.session_state.route_safety,
        "emergency_status": st.session_state.emergency_status,
        "status": "sent" if st.session_state.network_status == "Online" else "queued"
    }


def send_or_queue_alerts(reason):
    st.session_state.emergency_status = f"Triggered by {reason}"
    st.session_state.last_alert_time = now_str()
    alerts = [
        build_alert("Emergency Contact 1", st.session_state.contact_1_name or "Contact 1"),
        build_alert("Emergency Contact 2", st.session_state.contact_2_name or "Contact 2"),
        build_alert("Emergency Contact 3", st.session_state.contact_3_name or "Contact 3"),
        build_alert("Police", st.session_state.police_station_name),
        build_alert("Hospital", st.session_state.hospital_name),
    ]
    if st.session_state.network_status == "Online":
        DB["alerts"].extend(alerts)
        save_db(DB)
    else:
        st.session_state.queued_alerts.extend(alerts)
    return alerts


def flush_queued_alerts():
    if st.session_state.queued_alerts:
        DB["alerts"].extend(st.session_state.queued_alerts)
        count = len(st.session_state.queued_alerts)
        st.session_state.queued_alerts = []
        save_db(DB)
        return count
    return 0


def trigger_emergency(reason, fearful=False):
    if fearful:
        st.session_state.route_safety = "Critical Emergency"
    st.session_state.alarm_active = True
    speak_async("Emergency alert triggered. Contacting police, hospital and emergency contacts.")
    return send_or_queue_alerts(reason)


def log_route():
    DB["route_logs"].append({
        "mobile_number": st.session_state.mobile_number,
        "destination": st.session_state.destination_name,
        "route_safety": st.session_state.route_safety,
        "reason": st.session_state.route_reason,
        "timestamp": now_str()
    })
    save_db(DB)


def log_incident(report):
    DB["incidents"].append(report)
    save_db(DB)


def route_path_df():
    return pd.DataFrame([
        {"lat": st.session_state.latitude, "lon": st.session_state.longitude},
        {"lat": (st.session_state.latitude + st.session_state.destination_lat) / 2,
         "lon": (st.session_state.longitude + st.session_state.destination_lon) / 2},
        {"lat": st.session_state.destination_lat, "lon": st.session_state.destination_lon},
    ])


def zone_points_df():
    return pd.DataFrame([
        {"name": "📍 Your Location", "lat": st.session_state.latitude, "lon": st.session_state.longitude, "color": [0, 240, 255], "radius": 130},
        {"name": "🏁 Destination", "lat": st.session_state.destination_lat, "lon": st.session_state.destination_lon, "color": [0, 230, 118], "radius": 130},
        {"name": "✅ High Safe Zone", "lat": st.session_state.latitude + 0.004, "lon": st.session_state.longitude + 0.003, "color": [0, 200, 0], "radius": 180},
        {"name": "⚠️ Low Safe Zone",  "lat": st.session_state.latitude + 0.006, "lon": st.session_state.longitude - 0.002, "color": [255, 200, 0], "radius": 180},
        {"name": "🔴 Risky Area",     "lat": st.session_state.latitude - 0.004, "lon": st.session_state.longitude + 0.005, "color": [255, 59, 92], "radius": 180},
    ])


def show_map():
    points = zone_points_df()
    path_df = route_path_df()
    scatter = pdk.Layer("ScatterplotLayer", data=points, get_position="[lon, lat]",
                        get_fill_color="color", get_radius="radius", pickable=True)
    path_layer = pdk.Layer("PathLayer",
                           data=[{"path": path_df[["lon", "lat"]].values.tolist()}],
                           get_path="path", get_color=[0, 240, 255], width_scale=15, width_min_pixels=4)
    view_state = pdk.ViewState(latitude=st.session_state.latitude, longitude=st.session_state.longitude,
                               zoom=13, pitch=30)
    deck = pdk.Deck(map_style="mapbox://styles/mapbox/dark-v10",
                    initial_view_state=view_state, layers=[path_layer, scatter],
                    tooltip={"text": "{name}", "style": {"backgroundColor": "#0d1623", "color": "#00f0ff",
                                                          "border": "1px solid rgba(0,240,255,0.3)"}})
    st.pydeck_chart(deck)


# -------------------------
# ALARM (audio)
# -------------------------
def play_alarm_js(emergency=False):
    freq = 1200 if emergency else 900
    duration = 0.4 if emergency else 0.25
    reps = 6 if emergency else 3
    beep_calls = "".join(f"setTimeout(beep, {i * 400});\n" for i in range(reps))
    st.components.v1.html(f"""
    <script>
    try {{
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        function beep(){{
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'square';
            osc.frequency.value = {freq};
            gain.gain.value = 0.3;
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + {duration});
            osc.stop(ctx.currentTime + {duration});
        }}
        {beep_calls}
    }} catch(e) {{ console.log('Audio error:', e); }}
    </script>""", height=0)


def play_neighbor_alarm_js():
    """Loud, attention-seeking alarm to attract nearby neighbours."""
    st.components.v1.html("""
    <script>
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        let t = ctx.currentTime;
        const freqs = [880, 1100, 660, 1320, 440, 990, 770, 1210];
        freqs.forEach((f, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.value = f;
            gain.gain.setValueAtTime(0.5, t + i * 0.3);
            gain.gain.exponentialRampToValueAtTime(0.001, t + i * 0.3 + 0.28);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start(t + i * 0.3);
            osc.stop(t + i * 0.3 + 0.3);
        });
        // Repeat 3 times
        for (let rep = 1; rep < 3; rep++) {
            freqs.forEach((f, i) => {
                const osc2 = ctx.createOscillator();
                const g2 = ctx.createGain();
                osc2.type = 'sawtooth';
                osc2.frequency.value = f;
                g2.gain.setValueAtTime(0.5, t + rep * 2.4 + i * 0.3);
                g2.gain.exponentialRampToValueAtTime(0.001, t + rep * 2.4 + i * 0.3 + 0.28);
                osc2.connect(g2);
                g2.connect(ctx.destination);
                osc2.start(t + rep * 2.4 + i * 0.3);
                osc2.stop(t + rep * 2.4 + i * 0.3 + 0.3);
            });
        }
    } catch(e) { console.log('Alarm error:', e); }
    </script>""", height=0)


def show_alarm_ui():
    if st.session_state.alarm_active:
        st.markdown("""
        <div class="alert-notification emergency-pulse">
            <div class="alert-title">🚨 EMERGENCY ALARM ACTIVE</div>
            <div class="alert-body">
                Alert sent to: Emergency Contacts • Police • Hospital Ambulance<br>
                <small style="color:#ff7a7a;">Your location is being shared in real-time</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        play_alarm_js(emergency=True)
        if st.button("🔕 Stop Alarm", key="stop_alarm_btn"):
            st.session_state.alarm_active = False
            speak_async("Alarm stopped. Stay safe.")
            st.rerun()


# -------------------------
# BROWSER TTS
# -------------------------
def speak_browser(text: str, key: str = "speak"):
    st.components.v1.html(f"""
    <script>
    try {{
        const msg = new SpeechSynthesisUtterance({json.dumps(text)});
        msg.rate = 0.95; msg.pitch = 1.0; msg.lang = 'en-US';
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
    }} catch(e) {{ console.log('TTS error:', e); }}
    </script>""", height=0)


def speak_direction(text: str):
    """Speak navigation direction clearly."""
    st.components.v1.html(f"""
    <script>
    try {{
        const msg = new SpeechSynthesisUtterance({json.dumps(text)});
        msg.rate = 0.85; msg.pitch = 1.1; msg.volume = 1.0; msg.lang = 'en-US';
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(msg);
    }} catch(e) {{ console.log('Nav TTS error:', e); }}
    </script>""", height=0)


# -------------------------
# GOOGLE MAPS LIVE EMBED
# -------------------------
def show_google_maps_route(src_lat, src_lon, dst_lat, dst_lon, mode="driving"):
    """Embed a Google Maps directions iframe."""
    maps_url = get_google_maps_directions_url(src_lat, src_lon, dst_lat, dst_lon)
    st.markdown(f"""
    <div style="margin: 0.5rem 0;">
        <a href="{maps_url}" target="_blank"
           style="display:inline-flex; align-items:center; gap:0.5rem; background:linear-gradient(135deg,#0d47a1,#1565c0);
                  color:white; padding:0.5rem 1.2rem; border-radius:8px; text-decoration:none;
                  font-family:'Exo 2',sans-serif; font-weight:700; font-size:0.85rem; letter-spacing:1px;">
            🗺️ Open Route in Google Maps
        </a>
        <span style="color:#8898aa; font-size:0.75rem; margin-left:1rem;">↗ Opens in new tab with live navigation</span>
    </div>
    """, unsafe_allow_html=True)


def show_location_permission_request():
    """JS to request browser geolocation and return coords to Streamlit via query params."""
    st.components.v1.html("""
    <script>
    function requestLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                function(pos) {
                    const lat = pos.coords.latitude.toFixed(6);
                    const lon = pos.coords.longitude.toFixed(6);
                    const url = new URL(window.parent.location.href);
                    url.searchParams.set('lat', lat);
                    url.searchParams.set('lon', lon);
                    window.parent.location.href = url.toString();
                },
                function(err) {
                    alert('Location access denied or unavailable: ' + err.message);
                },
                {enableHighAccuracy: true, timeout: 10000}
            );
        } else {
            alert('Geolocation is not supported by your browser.');
        }
    }
    </script>
    <button onclick="requestLocation()"
        style="background:linear-gradient(135deg,#e91e8c,#b5136a); color:white; border:none;
               border-radius:8px; padding:0.7rem 1.5rem; font-family:'Exo 2',sans-serif;
               font-weight:700; font-size:0.9rem; cursor:pointer; letter-spacing:1px;
               box-shadow:0 4px 15px rgba(233,30,140,0.4);">
        📍 Allow Location Access
    </button>
    <p style="color:#8898aa; font-size:0.78rem; margin-top:0.5rem;">
        Tap above and allow browser location permission to detect your current position.
    </p>
    """, height=100)


def show_camera_light_detection():
    """Camera-based ambient light detection via JS."""
    st.markdown("""
    <div style="background:rgba(0,240,255,0.04); border:1px solid rgba(0,240,255,0.2);
                border-radius:12px; padding:1rem 1.2rem; margin-bottom:1rem;">
        <div style="color:#00f0ff; font-family:'Orbitron',monospace; font-size:0.85rem;
                    font-weight:700; margin-bottom:0.5rem;">📷 CAMERA LIGHT DETECTION</div>
        <div style="color:#8898aa; font-size:0.8rem; margin-bottom:1rem;">
            Uses your device camera to analyze ambient light on your current route.
            Click below to grant camera access.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.components.v1.html("""
    <style>
    #lightResult { margin-top:10px; padding:10px; border-radius:8px; font-family:'Exo 2',sans-serif; font-size:1rem; }
    #startCamBtn {
        background: linear-gradient(135deg,#e91e8c,#b5136a);
        color:white; border:none; border-radius:8px; padding:0.6rem 1.4rem;
        font-family:'Exo 2',sans-serif; font-weight:700; cursor:pointer;
        letter-spacing:1px; box-shadow:0 4px 15px rgba(233,30,140,0.4);
    }
    #stopCamBtn {
        background: linear-gradient(135deg,#333,#222);
        color:#8898aa; border:1px solid rgba(255,255,255,0.1); border-radius:8px;
        padding:0.6rem 1.4rem; font-family:'Exo 2',sans-serif; font-weight:700;
        cursor:pointer; letter-spacing:1px; margin-left:8px;
    }
    video { border-radius:8px; border:1px solid rgba(0,240,255,0.2); max-width:100%; }
    canvas { display:none; }
    </style>

    <button id="startCamBtn" onclick="startCamera()">📷 Allow Camera & Detect Light</button>
    <button id="stopCamBtn" onclick="stopCamera()" style="display:none;">⏹ Stop Camera</button>
    <br><br>
    <video id="camVideo" autoplay playsinline width="320" height="180" style="display:none;"></video>
    <canvas id="camCanvas" width="320" height="180"></canvas>
    <div id="lightResult"></div>

    <script>
    let stream = null;
    let analyzeInterval = null;

    function startCamera() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            document.getElementById('lightResult').innerHTML =
                '<span style="color:#ff3b5c;">⚠️ Camera not supported on this device/browser.</span>';
            return;
        }
        navigator.mediaDevices.getUserMedia({video: {facingMode: 'environment'}})
        .then(function(s) {
            stream = s;
            const video = document.getElementById('camVideo');
            video.srcObject = s;
            video.style.display = 'block';
            document.getElementById('startCamBtn').style.display = 'none';
            document.getElementById('stopCamBtn').style.display = 'inline-block';
            analyzeInterval = setInterval(analyzeLight, 1500);
        })
        .catch(function(err) {
            document.getElementById('lightResult').innerHTML =
                '<span style="color:#ff3b5c;">❌ Camera access denied: ' + err.message + '</span>';
        });
    }

    function stopCamera() {
        if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null; }
        clearInterval(analyzeInterval);
        document.getElementById('camVideo').style.display = 'none';
        document.getElementById('startCamBtn').style.display = 'inline-block';
        document.getElementById('stopCamBtn').style.display = 'none';
        document.getElementById('lightResult').innerHTML = '<span style="color:#8898aa;">Camera stopped.</span>';
    }

    function analyzeLight() {
        const video = document.getElementById('camVideo');
        const canvas = document.getElementById('camCanvas');
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;
        let total = 0;
        for (let i = 0; i < data.length; i += 4) {
            total += 0.299 * data[i] + 0.587 * data[i+1] + 0.114 * data[i+2];
        }
        const avg = total / (data.length / 4);
        let status, color, icon;
        if (avg > 170) { status = 'Bright Area — Safe'; color = '#00e676'; icon = '☀️'; }
        else if (avg > 100) { status = 'Moderate Light — Caution'; color = '#ffab00'; icon = '🌤️'; }
        else { status = 'Low Light / Dark — Risky'; color = '#ff3b5c'; icon = '🌑'; }

        document.getElementById('lightResult').innerHTML = `
            <div style="background:rgba(0,0,0,0.3); border:1px solid ${color}40; border-radius:8px;
                        padding:0.8rem; color:${color}; font-weight:700;">
                ${icon} Brightness: ${avg.toFixed(0)}/255 — ${status}
                <div style="height:6px; background:#111; border-radius:3px; margin-top:6px; overflow:hidden;">
                    <div style="height:100%; width:${Math.min(avg/255*100,100).toFixed(0)}%;
                                background:${color}; border-radius:3px; transition:width 0.5s;"></div>
                </div>
            </div>`;
    }
    </script>
    """, height=380)


# -------------------------
# ROUTE SAFETY WITH CRIME DATA
# -------------------------
# Simulated crime hotspot data for Coimbatore region
CRIME_HOTSPOTS = [
    {"name": "RS Puram Night Zone", "lat": 11.0120, "lon": 76.9500, "type": "theft", "severity": "high"},
    {"name": "Gandhipuram Corridor", "lat": 11.0170, "lon": 76.9610, "type": "harassment", "severity": "medium"},
    {"name": "Singanallur Junction", "lat": 11.0050, "lon": 77.0200, "type": "accident", "severity": "high"},
    {"name": "Peelamedu Stretch",    "lat": 11.0250, "lon": 77.0050, "type": "theft", "severity": "medium"},
    {"name": "Saibaba Colony",       "lat": 11.0310, "lon": 76.9400, "type": "harassment", "severity": "low"},
    {"name": "Ukkadam Market",       "lat": 10.9980, "lon": 76.9720, "type": "theft", "severity": "high"},
    {"name": "Kavundampalayam",      "lat": 11.0450, "lon": 76.9550, "type": "accident", "severity": "medium"},
]

ROUTE_OPTIONS = [
    {
        "id": "A",
        "name": "Route A — Main Road (Fastest)",
        "via": "Gandhipuram → RS Puram → Peelamedu",
        "distance": "6.4 km",
        "time": "18 min",
        "crime_score": 7,
        "safety": "Low Safe",
        "incidents": ["2 theft reports last month", "1 harassment incident"],
        "color": "#ffab00"
    },
    {
        "id": "B",
        "name": "Route B — Bypass Road (Recommended)",
        "via": "Saibaba Colony → Avinashi Rd → Bypass",
        "distance": "8.1 km",
        "time": "22 min",
        "crime_score": 2,
        "safety": "High Safe",
        "incidents": ["No major incidents in 3 months", "Well-lit stretch"],
        "color": "#00e676"
    },
    {
        "id": "C",
        "name": "Route C — Ukkadam Shortcut",
        "via": "Ukkadam → Singanallur → Peelamedu",
        "distance": "5.2 km",
        "time": "16 min",
        "crime_score": 11,
        "safety": "Risky Area",
        "incidents": ["3 theft cases", "Accident-prone zone", "Poor lighting"],
        "color": "#ff3b5c"
    },
]

NAV_STEPS = {
    "A": [
        {"arrow": "⬆️", "instruction": "Head north on Town Hall Road", "distance": "200 m"},
        {"arrow": "↰", "instruction": "Turn left onto Gandhipuram Main Street", "distance": "800 m"},
        {"arrow": "↱", "instruction": "Turn right at RS Puram signal", "distance": "1.2 km"},
        {"arrow": "⬆️", "instruction": "Continue straight on Nehru Street", "distance": "600 m"},
        {"arrow": "↱", "instruction": "Turn right onto Avinashi Road", "distance": "2.1 km"},
        {"arrow": "↰", "instruction": "Turn left at Peelamedu junction", "distance": "900 m"},
        {"arrow": "🏁", "instruction": "You have arrived at your destination", "distance": ""},
    ],
    "B": [
        {"arrow": "⬆️", "instruction": "Head north — take Saibaba Colony Road", "distance": "400 m"},
        {"arrow": "↱", "instruction": "Turn right onto Avinashi Road (well-lit)", "distance": "2.5 km"},
        {"arrow": "⬆️", "instruction": "Continue on Bypass Road — stay straight", "distance": "3.2 km"},
        {"arrow": "↰", "instruction": "Turn left at main junction", "distance": "600 m"},
        {"arrow": "🏁", "instruction": "You have arrived safely at your destination", "distance": ""},
    ],
    "C": [
        {"arrow": "⬆️", "instruction": "Head south toward Ukkadam Market", "distance": "300 m"},
        {"arrow": "↱", "instruction": "Turn right — ⚠️ High theft zone, stay alert", "distance": "1.1 km"},
        {"arrow": "↰", "instruction": "Turn left at Singanallur — 🚨 Accident-prone area", "distance": "2.0 km"},
        {"arrow": "⬆️", "instruction": "Straight ahead to Peelamedu", "distance": "800 m"},
        {"arrow": "🏁", "instruction": "Arrived. Note: This route passes risky areas.", "distance": ""},
    ],
}


def show_route_options():
    """Show three route options with safety scores based on crime history."""
    st.markdown("""
    <div style="color:#00f0ff; font-family:'Orbitron',monospace; font-size:0.85rem;
                font-weight:700; letter-spacing:1px; margin-bottom:1rem;">
        🗺️ ROUTE OPTIONS — SAFETY ANALYSIS (Based on Crime & Incident History)
    </div>
    """, unsafe_allow_html=True)

    for route in ROUTE_OPTIONS:
        badge_class = "badge-safe" if route["safety"] == "High Safe" else \
                      "badge-warn" if route["safety"] == "Low Safe" else "badge-danger"
        incidents_html = "".join(f"<li style='color:#8898aa;'>{i}</li>" for i in route["incidents"])
        safety_pct = max(0, 100 - route["crime_score"] * 8)
        st.markdown(f"""
        <div class="she-card" style="border-left:4px solid {route['color']}; margin-bottom:0.8rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                <div style="font-family:'Orbitron',monospace; font-weight:700; font-size:0.95rem;">
                    {route['name']}
                </div>
                <span class="badge {badge_class}">{route['safety']}</span>
            </div>
            <div style="font-size:0.82rem; color:#8898aa; margin-bottom:0.5rem;">
                📍 Via: {route['via']}
            </div>
            <div style="display:flex; gap:1.5rem; font-size:0.82rem; margin-bottom:0.6rem;">
                <span>🛣️ {route['distance']}</span>
                <span>⏱️ {route['time']}</span>
                <span>⚠️ Crime Score: {route['crime_score']}/10</span>
            </div>
            <div style="height:6px; background:#111; border-radius:3px; margin-bottom:0.6rem; overflow:hidden;">
                <div style="height:100%; width:{safety_pct}%; background:{route['color']};
                            border-radius:3px; transition:width 0.5s;"></div>
            </div>
            <ul style="margin:0; padding-left:1.2rem; font-size:0.78rem;">
                {incidents_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    return ROUTE_OPTIONS


def show_navigation_steps(route_id):
    """Voice-guided step-by-step navigation."""
    steps = NAV_STEPS.get(route_id, NAV_STEPS["B"])
    idx = st.session_state.current_step_index

    st.markdown(f"""
    <div style="background:rgba(0,240,255,0.05); border:1px solid rgba(0,240,255,0.2);
                border-radius:12px; padding:1rem; margin-bottom:1rem;">
        <div style="color:#00f0ff; font-family:'Orbitron',monospace; font-size:0.8rem;
                    font-weight:700; letter-spacing:1px; margin-bottom:0.5rem;">
            🎙️ VOICE NAVIGATION — Step {idx+1} of {len(steps)}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    progress = (idx + 1) / len(steps)
    st.progress(progress)

    # Current step highlighted
    if idx < len(steps):
        step = steps[idx]
        st.markdown(f"""
        <div style="background:linear-gradient(135deg, rgba(0,240,255,0.12), rgba(233,30,140,0.06));
                    border:2px solid rgba(0,240,255,0.4); border-radius:14px; padding:1.5rem;
                    text-align:center; margin-bottom:1rem;">
            <div style="font-size:3rem; margin-bottom:0.5rem;">{step['arrow']}</div>
            <div style="font-family:'Orbitron',monospace; font-size:1.1rem; color:#e8f0fe;
                        font-weight:700; margin-bottom:0.3rem;">{step['instruction']}</div>
            <div style="color:#8898aa; font-size:0.85rem;">{step['distance']}</div>
        </div>
        """, unsafe_allow_html=True)
        speak_direction(step['instruction'])

    # Upcoming steps
    if idx + 1 < len(steps):
        st.markdown('<div style="color:#8898aa; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.4rem;">Upcoming Steps</div>', unsafe_allow_html=True)
        for j, step in enumerate(steps[idx + 1: idx + 3], start=idx + 1):
            st.markdown(f"""
            <div class="nav-direction" style="opacity:0.6;">
                <div class="nav-arrow">{step['arrow']}</div>
                <div class="nav-text">
                    <div style="font-size:0.85rem; color:#e8f0fe;">{step['instruction']}</div>
                    <div class="nav-dist">{step['distance']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    nc1, nc2, nc3 = st.columns(3)
    if nc1.button("⏮ Previous", key="nav_prev") and idx > 0:
        st.session_state.current_step_index -= 1
        st.rerun()
    if nc2.button("⏭ Next Step", key="nav_next") and idx < len(steps) - 1:
        st.session_state.current_step_index += 1
        st.rerun()
    if nc3.button("🔁 Repeat", key="nav_repeat"):
        if idx < len(steps):
            speak_direction(steps[idx]['instruction'])
        st.rerun()

    if idx == len(steps) - 1:
        st.success("✅ You have arrived at your destination safely!")
        speak_direction("You have arrived at your destination. Stay safe.")
        if st.button("🏁 End Navigation", key="end_nav"):
            st.session_state.navigation_active = False
            st.session_state.current_step_index = 0
            st.rerun()


def show_crime_heatmap():
    """Show crime/incident hotspots on the pydeck map."""
    hotspot_df = pd.DataFrame(CRIME_HOTSPOTS)
    hotspot_df["color"] = hotspot_df["severity"].map({
        "high": [255, 59, 92],
        "medium": [255, 171, 0],
        "low": [0, 230, 118]
    })
    hotspot_df["radius"] = hotspot_df["severity"].map({"high": 300, "medium": 220, "low": 150})

    path_df = route_path_df()
    scatter_route = pdk.Layer("ScatterplotLayer",
        data=pd.DataFrame([
            {"name": "📍 You", "lat": st.session_state.latitude, "lon": st.session_state.longitude,
             "color": [0, 240, 255], "radius": 150},
            {"name": "🏁 Dest", "lat": st.session_state.destination_lat, "lon": st.session_state.destination_lon,
             "color": [0, 230, 118], "radius": 150},
        ]),
        get_position="[lon, lat]", get_fill_color="color", get_radius="radius", pickable=True)

    hotspot_layer = pdk.Layer("ScatterplotLayer", data=hotspot_df,
        get_position="[lon, lat]", get_fill_color="color", get_radius="radius",
        opacity=0.6, pickable=True)

    path_layer = pdk.Layer("PathLayer",
        data=[{"path": path_df[["lon", "lat"]].values.tolist()}],
        get_path="path", get_color=[0, 240, 255], width_scale=15, width_min_pixels=3)

    view = pdk.ViewState(latitude=st.session_state.latitude, longitude=st.session_state.longitude,
                         zoom=12, pitch=40)
    deck = pdk.Deck(map_style="mapbox://styles/mapbox/dark-v10",
                    initial_view_state=view, layers=[path_layer, hotspot_layer, scatter_route],
                    tooltip={"text": "{name} — {type} ({severity})",
                             "style": {"backgroundColor": "#0d1623", "color": "#ff3b5c",
                                       "border": "1px solid rgba(255,59,92,0.4)"}})
    st.pydeck_chart(deck)


# -------------------------
# INCIDENT MEDIA CAPTURE
# -------------------------
def show_incident_media_capture():
    """Browser-based camera capture for incident evidence."""
    st.markdown("""
    <div style="background:rgba(255,59,92,0.06); border:1px solid rgba(255,59,92,0.3);
                border-radius:12px; padding:1rem 1.2rem; margin-bottom:1rem;">
        <div style="color:#ff3b5c; font-family:'Orbitron',monospace; font-size:0.85rem;
                    font-weight:700; margin-bottom:0.4rem;">📸 INCIDENT EVIDENCE CAPTURE</div>
        <div style="color:#8898aa; font-size:0.8rem;">
            Capture photo or video evidence of the incident. Files are saved locally as proof.
            Allow camera access when prompted.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.components.v1.html("""
    <style>
    .cap-btn {
        background: linear-gradient(135deg,#b5136a,#e91e8c);
        color: white; border: none; border-radius: 8px;
        padding: 0.6rem 1.2rem; font-family: 'Exo 2', sans-serif;
        font-weight: 700; cursor: pointer; margin-right: 8px;
        letter-spacing: 1px; font-size: 0.85rem;
    }
    .cap-btn.stop { background: linear-gradient(135deg,#333,#555); color:#aaa; }
    #incidentVideo { border-radius:8px; border:1px solid rgba(255,59,92,0.3); max-width:100%; }
    #capturedImage { border-radius:8px; border:1px solid rgba(0,230,118,0.3); max-width:100%; margin-top:8px; }
    #recStatus { color:#ff3b5c; font-family:'Exo 2',sans-serif; font-size:0.85rem; margin-top:8px; }
    canvas#snapCanvas { display:none; }
    </style>

    <button class="cap-btn" onclick="startCap()">📷 Start Camera</button>
    <button class="cap-btn stop" id="snapBtn" onclick="capturePhoto()" style="display:none;">📸 Take Photo</button>
    <button class="cap-btn" id="recBtn" onclick="startRec()" style="display:none; background:linear-gradient(135deg,#7f0000,#c62828);">🔴 Record Video</button>
    <button class="cap-btn stop" id="stopRecBtn" onclick="stopRec()" style="display:none;">⏹ Stop & Save</button>
    <button class="cap-btn stop" onclick="stopCap()" id="stopCapBtn" style="display:none;">✖ Close Camera</button>

    <br><br>
    <video id="incidentVideo" autoplay playsinline width="360" height="220" style="display:none;"></video>
    <canvas id="snapCanvas" width="360" height="220"></canvas>
    <div id="recStatus"></div>
    <img id="capturedImage" style="display:none;"/>
    <div id="downloadLinks"></div>

    <script>
    let capStream = null;
    let mediaRecorder = null;
    let recordedChunks = [];

    function startCap() {
        navigator.mediaDevices.getUserMedia({video: true, audio: true})
        .then(s => {
            capStream = s;
            const v = document.getElementById('incidentVideo');
            v.srcObject = s; v.style.display = 'block';
            document.getElementById('snapBtn').style.display = 'inline-block';
            document.getElementById('recBtn').style.display = 'inline-block';
            document.getElementById('stopCapBtn').style.display = 'inline-block';
            document.getElementById('recStatus').innerText = '✅ Camera ready. Take photo or record video.';
        })
        .catch(err => {
            document.getElementById('recStatus').innerHTML =
                '<span style="color:#ff3b5c;">❌ Camera denied: ' + err.message + '</span>';
        });
    }

    function capturePhoto() {
        const v = document.getElementById('incidentVideo');
        const c = document.getElementById('snapCanvas');
        const ctx = c.getContext('2d');
        ctx.drawImage(v, 0, 0, c.width, c.height);
        const img = document.getElementById('capturedImage');
        const dataURL = c.toDataURL('image/jpeg', 0.92);
        img.src = dataURL; img.style.display = 'block';

        // Create download link
        const a = document.createElement('a');
        const ts = new Date().toISOString().replace(/[:.]/g,'-');
        a.href = dataURL;
        a.download = 'incident_' + ts + '.jpg';
        a.style.cssText = 'display:inline-block; margin-top:8px; padding:6px 14px; background:#00e676; color:#000; border-radius:6px; font-weight:700; text-decoration:none; font-size:0.82rem;';
        a.innerText = '⬇️ Save Photo to Gallery';
        document.getElementById('downloadLinks').appendChild(a);
        document.getElementById('recStatus').innerHTML =
            '<span style="color:#00e676;">✅ Photo captured! Click Save to store in your gallery/photos.</span>';
    }

    function startRec() {
        recordedChunks = [];
        mediaRecorder = new MediaRecorder(capStream, {mimeType: 'video/webm;codecs=vp9'});
        mediaRecorder.ondataavailable = e => { if (e.data.size > 0) recordedChunks.push(e.data); };
        mediaRecorder.onstop = saveVideo;
        mediaRecorder.start();
        document.getElementById('recBtn').style.display = 'none';
        document.getElementById('stopRecBtn').style.display = 'inline-block';
        document.getElementById('recStatus').innerHTML =
            '<span style="color:#ff3b5c; animation: blink 1s infinite;">🔴 Recording...</span>';
    }

    function stopRec() {
        mediaRecorder.stop();
        document.getElementById('stopRecBtn').style.display = 'none';
        document.getElementById('recBtn').style.display = 'inline-block';
    }

    function saveVideo() {
        const blob = new Blob(recordedChunks, {type: 'video/webm'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        const ts = new Date().toISOString().replace(/[:.]/g,'-');
        a.href = url;
        a.download = 'incident_video_' + ts + '.webm';
        a.style.cssText = 'display:inline-block; margin-top:8px; padding:6px 14px; background:#e91e8c; color:white; border-radius:6px; font-weight:700; text-decoration:none; font-size:0.82rem;';
        a.innerText = '⬇️ Save Video to Gallery';
        document.getElementById('downloadLinks').appendChild(a);
        document.getElementById('recStatus').innerHTML =
            '<span style="color:#00e676;">✅ Video recorded! Click Save to store in your photos/gallery.</span>';
    }

    function stopCap() {
        if (capStream) { capStream.getTracks().forEach(t => t.stop()); capStream = null; }
        document.getElementById('incidentVideo').style.display = 'none';
        ['snapBtn','recBtn','stopRecBtn','stopCapBtn'].forEach(id => {
            document.getElementById(id).style.display = 'none';
        });
        document.getElementById('recStatus').innerText = 'Camera closed.';
    }
    </script>
    """, height=460)


# -------------------------
# NEIGHBOR ALARM
# -------------------------
def show_neighbor_alarm():
    """Emergency alarm to attract attention of nearby neighbors."""
    st.markdown("""
    <div class="she-card" style="border-color:rgba(255,59,92,0.4); text-align:center;">
        <div style="color:#ff3b5c; font-family:'Orbitron',monospace; font-size:0.9rem;
                    font-weight:700; margin-bottom:0.5rem;">🔊 NEIGHBOR ATTENTION ALARM</div>
        <div style="color:#8898aa; font-size:0.82rem; margin-bottom:1rem;">
            Triggers a loud alarm sound to seek immediate help from people nearby.
            Use during physical danger when your phone cannot connect to emergency services.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    if col1.button("🔊 SOUND NEIGHBOR ALARM", key="neighbor_alarm_btn"):
        st.session_state.neighbor_alarm_active = True
        play_neighbor_alarm_js()
        speak_browser("Emergency! Help needed! Alerting nearby people now.")
        st.markdown("""
        <div class="alert-notification emergency-pulse" style="text-align:center; margin-top:0.5rem;">
            <div class="alert-title">🔊 ALARM SOUNDING — Seeking Neighbor Attention</div>
            <div class="alert-body">Loud alarm activated. Wave your phone to attract attention.</div>
        </div>
        """, unsafe_allow_html=True)

    if col2.button("🔕 Stop Neighbor Alarm", key="stop_neighbor_btn"):
        st.session_state.neighbor_alarm_active = False
        st.success("Alarm stopped.")


# -------------------------
# VOICE ASSISTANT BLOCK
# -------------------------
def voice_block(module_key: str, voice_guidance: str = ""):
    st.markdown(f"""
    <div class="voice-panel">
        <div style="font-family:'Orbitron',monospace; font-size:0.85rem; color:#00f0ff;
                    font-weight:700; margin-bottom:0.6rem; letter-spacing:1px;">🎙️ VOICE ASSISTANT</div>
        <div style="font-size:0.8rem; color:#8898aa; margin-bottom:0.8rem;">
            {voice_guidance or 'Speak a command or use distress word to trigger emergency'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    listening = st.session_state.listening_status == "Listening"
    status_color = "#00e676" if listening else "#8898aa"
    status_dot = "active" if listening else "inactive"

    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:0.5rem; margin:0.5rem 0;">
        <span class="voice-indicator {status_dot}"></span>
        <span style="color:{status_color}; font-size:0.82rem; font-weight:600;
                     text-transform:uppercase; letter-spacing:1px;">
            {st.session_state.listening_status}
        </span>
    </div>
    """, unsafe_allow_html=True)

    a, b = st.columns(2)
    if a.button("🎤 Start Listening", key=f"start_{module_key}"):
        st.session_state.listening_status = "Listening"
        speak_browser("Voice assistant activated. I am listening.")
        st.rerun()
    if b.button("⏹ Stop Listening", key=f"stop_{module_key}"):
        st.session_state.listening_status = "Not Listening"
        speak_browser("Voice assistant stopped.")
        st.rerun()

    recognized = st.text_input("💬 Voice Command / Type Here", key=f"voice_{module_key}",
                                placeholder="Say or type your command...")
    fearful = st.checkbox("😰 Fearful / Shivering Voice Detected", key=f"fear_{module_key}")

    if st.button(f"▶ Process Command", key=f"process_{module_key}"):
        st.session_state.recognized_speech = recognized
        if recognized.strip().lower() == st.session_state.distress_word.strip().lower() and st.session_state.distress_word:
            alerts = trigger_emergency(f"voice distress in {module_key}", fearful)
            speak_browser("Emergency triggered! Alerting police, hospital and your emergency contacts now.")
            return alerts
        else:
            speak_browser(f"Command received: {recognized}")
            st.info(f"✅ Voice command processed: {recognized}")
    return []


# -------------------------
# ALERT DISPLAY
# -------------------------
def show_alert_dispatch(alerts):
    st.markdown("""
    <div class="alert-notification" style="margin:1rem 0;">
        <div class="alert-title">📡 ALERTS DISPATCHED</div>
    </div>
    """, unsafe_allow_html=True)
    cols = st.columns(min(len(alerts), 3))
    icons = {"Emergency Contact 1": "👤", "Emergency Contact 2": "👤", "Emergency Contact 3": "👤",
             "Police": "🚔", "Hospital": "🚑"}
    colors = {"Emergency Contact 1": "#e91e8c", "Emergency Contact 2": "#e91e8c", "Emergency Contact 3": "#e91e8c",
              "Police": "#4fc3f7", "Hospital": "#ef5350"}
    for i, alert in enumerate(alerts):
        col = cols[i % 3]
        icon = icons.get(alert["recipient_type"], "📢")
        color = colors.get(alert["recipient_type"], "#00f0ff")
        col.markdown(f"""
        <div style="background:rgba(255,255,255,0.03); border:1px solid {color}40; border-left:3px solid {color};
                    border-radius:8px; padding:0.7rem; margin-bottom:0.4rem;">
            <div style="font-size:1.2rem; margin-bottom:0.2rem;">{icon}</div>
            <div style="color:{color}; font-size:0.75rem; font-weight:700; text-transform:uppercase;">{alert['recipient_type']}</div>
            <div style="color:#8898aa; font-size:0.72rem; margin-top:0.2rem;">{alert['recipient_name']}</div>
            <div style="color:#00e676; font-size:0.68rem; margin-top:0.2rem;">✓ {alert['status'].upper()}</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# LOGIN / REGISTER PAGES
# ============================================================
if not st.session_state.logged_in:

    st.markdown("""
    <div class="login-hero">
        <span class="hero-icon">🛡️</span>
        <h1>SheSense SafeRoute AI+</h1>
        <p>Advanced Women Safety Intelligence System</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="text-align:center; margin-bottom:1rem;"><span style="color:#8898aa; font-size:0.82rem; text-transform:uppercase; letter-spacing:2px;">Select Your Role</span></div>', unsafe_allow_html=True)

    rc1, rc2, rc3 = st.columns(3)
    roles = [
        ("rc1", "👩", "User", "Personal Safety & Emergency"),
        ("rc2", "🚔", "Police", "Law Enforcement Portal"),
        ("rc3", "🏥", "Hospital / Ambulance", "Medical Emergency Portal"),
    ]
    for col, (key, icon, name, desc) in zip([rc1, rc2, rc3], roles):
        selected_class = "selected" if st.session_state.selected_role == name else ""
        col.markdown(f"""
        <div class="role-card {selected_class}">
            <span class="role-icon">{icon}</span>
            <div class="role-name">{name}</div>
            <div class="role-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        if col.button(f"Select {name}", key=f"sel_{key}"):
            st.session_state.selected_role = name
            st.rerun()

    st.markdown('<div class="she-divider"></div>', unsafe_allow_html=True)

    role = st.session_state.selected_role
    tab_login, tab_register = st.tabs([f"🔑 Login as {role}", f"📝 Register as {role}"])

    with tab_login:
        if role == "User":
            st.markdown('<h3 style="color:#e91e8c!important; border:none!important; padding:0!important;">User Login</h3>', unsafe_allow_html=True)
            lc1, lc2 = st.columns([1, 1])
            with lc1:
                st.markdown('<div class="she-card">', unsafe_allow_html=True)
                st.session_state.user_name = st.text_input("👤 Full Name", value=st.session_state.user_name, placeholder="Your name")
                st.session_state.mobile_number = st.text_input("📱 Mobile Number", value=st.session_state.mobile_number, placeholder="+91 XXXXXXXXXX")

                if st.button("📲 Send OTP"):
                    if validate_mobile(st.session_state.mobile_number):
                        otp = generate_otp()
                        st.session_state.generated_otp = otp
                        st.session_state.otp_sent = True
                        speak_browser(f"OTP sent to your mobile number.")
                        st.success(f"✅ OTP sent to {st.session_state.mobile_number}")
                        st.markdown(f'<div class="otp-section"><span style="color:#8898aa; font-size:0.75rem;">DEMO OTP:</span> <span style="font-family:Orbitron,monospace; font-size:1.2rem; color:#00f0ff; font-weight:700;">{otp}</span></div>', unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Enter a valid mobile number")

                if st.session_state.otp_sent:
                    entered_otp = st.text_input("🔢 Enter OTP", max_chars=6, placeholder="6-digit OTP")
                    if st.button("✅ Verify OTP"):
                        if entered_otp == st.session_state.generated_otp and entered_otp:
                            st.session_state.otp_verified = True
                            speak_browser("OTP verified. Please complete your profile setup.")
                            st.success("OTP verified!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid OTP")
                st.markdown('</div>', unsafe_allow_html=True)

            with lc2:
                if st.session_state.otp_verified:
                    st.markdown('<div class="she-card">', unsafe_allow_html=True)
                    st.markdown('<div style="color:#00f0ff; font-size:0.78rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.8rem;">Emergency Contacts & Setup</div>', unsafe_allow_html=True)
                    st.session_state.distress_word = st.text_input("🔑 Personal Distress Word", value=st.session_state.distress_word, placeholder="e.g. HELP123")
                    st.session_state.contact_1_name = st.text_input("Contact 1 Name", value=st.session_state.contact_1_name, placeholder="e.g. Mom")
                    st.session_state.contact_1_number = st.text_input("Contact 1 Number", value=st.session_state.contact_1_number)
                    st.session_state.contact_2_name = st.text_input("Contact 2 Name", value=st.session_state.contact_2_name)
                    st.session_state.contact_2_number = st.text_input("Contact 2 Number", value=st.session_state.contact_2_number)
                    st.session_state.contact_3_name = st.text_input("Contact 3 Name", value=st.session_state.contact_3_name)
                    st.session_state.contact_3_number = st.text_input("Contact 3 Number", value=st.session_state.contact_3_number)

                    if st.button("🚀 Save & Login"):
                        if st.session_state.distress_word.strip():
                            st.session_state.logged_in = True
                            st.session_state.user_role = "user"
                            persist_user()
                            speak_browser("Welcome to SheSense SafeRoute. You are now logged in and protected.")
                            st.rerun()
                        else:
                            st.warning("⚠️ Please set a distress word first")
                    st.markdown('</div>', unsafe_allow_html=True)

        elif role == "Police":
            st.markdown('<h3 style="color:#4fc3f7!important; border:none!important; padding:0!important;">Police Portal Login</h3>', unsafe_allow_html=True)
            pc1, _ = st.columns([1, 1])
            with pc1:
                st.markdown('<div class="she-card">', unsafe_allow_html=True)
                badge_id = st.text_input("🪪 Badge ID / Employee ID", placeholder="e.g. TN-CB-1234")
                mobile = st.text_input("📱 Registered Mobile", placeholder="+91 XXXXXXXXXX")
                station = st.text_input("🏢 Police Station Name", placeholder="e.g. Coimbatore Central")
                if st.button("🔐 Police Login"):
                    match = next((u for u in DB.get("police_users", []) if u.get("badge_id") == badge_id and u.get("mobile") == mobile), None)
                    if match or (badge_id and mobile and station):
                        st.session_state.logged_in = True
                        st.session_state.user_role = "police"
                        st.session_state.user_name = match.get("name", f"Officer [{badge_id}]") if match else f"Officer [{badge_id}]"
                        st.session_state.police_badge_id = badge_id
                        st.session_state.police_station = station
                        speak_browser("Welcome Officer. Police portal access granted.")
                        st.rerun()
                    else:
                        st.error("❌ Fill all fields to login")
                st.markdown('</div>', unsafe_allow_html=True)

        elif role == "Hospital / Ambulance":
            st.markdown('<h3 style="color:#ef5350!important; border:none!important; padding:0!important;">Hospital / Ambulance Login</h3>', unsafe_allow_html=True)
            hc1, _ = st.columns([1, 1])
            with hc1:
                st.markdown('<div class="she-card">', unsafe_allow_html=True)
                hosp_id = st.text_input("🆔 Staff / Ambulance ID", placeholder="e.g. HOSP-AMB-001")
                hosp_mobile = st.text_input("📱 Registered Mobile", placeholder="+91 XXXXXXXXXX")
                hosp_name = st.text_input("🏥 Hospital Name", placeholder="e.g. City Emergency Hospital")

                # Patient pre-registration for ambulance
                st.markdown('<div style="color:#8898aa; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; margin-top:1rem; margin-bottom:0.4rem;">Patient Details (for Pregnant/Emergency)</div>', unsafe_allow_html=True)
                amb_patient = st.text_input("👩 Patient Name", placeholder="Full name")
                amb_age = st.number_input("🎂 Patient Age", min_value=10, max_value=80, value=28)
                amb_due = st.text_input("📅 Due Date (if pregnant)", placeholder="DD/MM/YYYY")
                amb_blood = st.selectbox("🩸 Blood Group", ["Unknown", "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
                amb_comp = st.text_area("⚕️ Known Complications", placeholder="Diabetes, hypertension, etc.", height=60)

                if st.button("🔐 Hospital Login"):
                    if hosp_id and hosp_mobile and hosp_name:
                        st.session_state.logged_in = True
                        st.session_state.user_role = "hospital"
                        st.session_state.user_name = f"Staff [{hosp_id}]"
                        st.session_state.hospital_name = hosp_name
                        st.session_state.amb_patient_name = amb_patient
                        st.session_state.amb_patient_age = amb_age
                        st.session_state.amb_due_date = amb_due
                        st.session_state.amb_blood_group = amb_blood
                        st.session_state.amb_complications = amb_comp
                        speak_browser("Welcome. Hospital portal access granted.")
                        st.rerun()
                    else:
                        st.error("❌ Fill all required fields")
                st.markdown('</div>', unsafe_allow_html=True)

    with tab_register:
        if role == "User":
            st.markdown('<h3 style="color:#e91e8c!important; border:none!important; padding:0!important;">Create User Account</h3>', unsafe_allow_html=True)
            r1, r2 = st.columns(2)
            with r1:
                st.markdown('<div class="she-card">', unsafe_allow_html=True)
                reg_name = st.text_input("👤 Full Name", key="reg_name", placeholder="Your full name")
                reg_mobile = st.text_input("📱 Mobile Number", key="reg_mobile", placeholder="+91 XXXXXXXXXX")
                reg_age = st.number_input("🎂 Age", min_value=10, max_value=100, value=25, key="reg_age")
                reg_distress = st.text_input("🔑 Distress Word", key="reg_distress", placeholder="Secret word to trigger SOS")
                if st.button("📲 Send OTP to Register"):
                    if validate_mobile(reg_mobile):
                        otp = generate_otp()
                        st.session_state.generated_otp = otp
                        st.session_state.otp_sent = True
                        st.success(f"OTP sent!")
                        st.markdown(f'<div class="otp-section"><span style="color:#8898aa; font-size:0.75rem;">DEMO OTP:</span> <span style="font-family:Orbitron,monospace; font-size:1.2rem; color:#00f0ff;">{otp}</span></div>', unsafe_allow_html=True)
                    else:
                        st.warning("Enter valid mobile number")
                if st.session_state.otp_sent:
                    reg_otp = st.text_input("🔢 OTP", key="reg_otp_input", max_chars=6)
                    if st.button("✅ Verify & Complete Registration"):
                        if reg_otp == st.session_state.generated_otp and reg_name and reg_distress:
                            new_user = {"mobile_number": reg_mobile, "user_name": reg_name,
                                        "distress_word": reg_distress, "contacts": [], "saved_at": now_str()}
                            DB["users"].append(new_user)
                            save_db(DB)
                            st.success("🎉 Registration successful! Please login.")
                            speak_browser("Registration successful. Please login.")
                        else:
                            st.error("Invalid OTP or missing fields")
                st.markdown('</div>', unsafe_allow_html=True)

        elif role == "Police":
            st.markdown('<h3 style="color:#4fc3f7!important; border:none!important; padding:0!important;">Police Officer Registration</h3>', unsafe_allow_html=True)
            p1, p2 = st.columns(2)
            with p1:
                st.markdown('<div class="she-card">', unsafe_allow_html=True)
                pr_name = st.text_input("👤 Officer Full Name", key="pr_name")
                pr_badge = st.text_input("🪪 Badge ID / Service Number", key="pr_badge")
                pr_rank = st.selectbox("🎖️ Rank", ["Constable", "Head Constable", "ASI", "SI", "Inspector", "DSP", "SP"], key="pr_rank")
                pr_station = st.text_input("🏢 Police Station", key="pr_station")
                pr_division = st.text_input("🗂️ Division / Branch", key="pr_division")
                pr_mobile = st.text_input("📱 Mobile Number", key="pr_mobile")
                if st.button("✅ Register as Police"):
                    if pr_name and pr_badge and pr_station and pr_mobile:
                        po = {"name": pr_name, "badge_id": pr_badge, "rank": pr_rank,
                              "station": pr_station, "division": pr_division,
                              "mobile": pr_mobile, "registered_at": now_str()}
                        DB.setdefault("police_users", []).append(po)
                        save_db(DB)
                        st.success("✅ Police registration successful!")
                        speak_browser("Police registration successful. You can now login.")
                    else:
                        st.error("Fill all required fields")
                st.markdown('</div>', unsafe_allow_html=True)

        elif role == "Hospital / Ambulance":
            st.markdown('<h3 style="color:#ef5350!important; border:none!important; padding:0!important;">Hospital / Ambulance Registration</h3>', unsafe_allow_html=True)
            h1, h2 = st.columns(2)
            with h1:
                st.markdown('<div class="she-card">', unsafe_allow_html=True)
                hr_name = st.text_input("👤 Staff Name", key="hr_name")
                hr_hosp = st.text_input("🏥 Hospital Name", key="hr_hosp")
                hr_dept = st.selectbox("🏨 Department", ["Emergency & Trauma", "ICU", "Ambulance Dispatch", "Maternity", "General"], key="hr_dept")
                hr_id = st.text_input("🆔 Staff / Vehicle ID", key="hr_id")
                hr_mobile = st.text_input("📱 Contact Number", key="hr_mobile")
                hr_address = st.text_input("📍 Hospital Address", key="hr_address")
                if st.button("✅ Register Hospital Staff"):
                    if hr_name and hr_hosp and hr_id and hr_mobile:
                        hu = {"name": hr_name, "hospital": hr_hosp, "dept": hr_dept, "staff_id": hr_id,
                              "mobile": hr_mobile, "address": hr_address, "registered_at": now_str()}
                        DB.setdefault("hospital_users", []).append(hu)
                        save_db(DB)
                        st.success("✅ Hospital registration successful!")
                        speak_browser("Hospital staff registration successful.")
                    else:
                        st.error("Fill all required fields")
                st.markdown('</div>', unsafe_allow_html=True)

    st.stop()


# ============================================================
# MAIN APP — POST LOGIN
# ============================================================

with st.sidebar:
    role_icon = {"user": "👩", "police": "🚔", "hospital": "🏥"}.get(st.session_state.user_role, "👤")
    role_label = {"user": "User", "police": "Police Officer", "hospital": "Hospital Staff"}.get(st.session_state.user_role, "User")
    st.markdown(f"""
    <div class="sidebar-user">
        <div class="user-name">{role_icon} {st.session_state.user_name or 'User'}</div>
        <div class="user-status">● Online • {role_label}</div>
        <div style="color:#8898aa; font-size:0.72rem; margin-top:0.3rem;">📱 {st.session_state.mobile_number or 'N/A'}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="color:#8898aa; font-size:0.7rem; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:0.4rem; padding-left:0.3rem;">Navigation</div>', unsafe_allow_html=True)

    if st.session_state.user_role == "police":
        modules = ["Police Dashboard", "Active Alerts", "Patrol Map", "Incident Reports", "Saved Data"]
    elif st.session_state.user_role == "hospital":
        modules = ["Hospital Dashboard", "Emergency Queue", "Ambulance Dispatch",
                   "Pregnant Route Checker", "Pregnant Emergencies", "Saved Data"]
    else:
        modules = ["Dashboard", "Route Planning", "Safety Monitor", "Emergency",
                   "Offline Mode", "Incident Recovery", "Pregnant Mode",
                   "Police Assistance", "Hospital Assistance",
                   "Camera Light Detection", "Saved Data"]

    module = st.radio("", modules, label_visibility="collapsed")

    st.markdown('<div class="she-divider"></div>', unsafe_allow_html=True)

    if st.session_state.user_role == "user":
        if st.button("🆘 QUICK SOS", key="sidebar_sos"):
            alerts = trigger_emergency("Sidebar Quick SOS")
            speak_browser("SOS Emergency! Alerting police, hospital and your emergency contacts now!")
            st.rerun()
        if st.button("🔊 NEIGHBOR ALARM", key="sidebar_neighbor"):
            play_neighbor_alarm_js()
            speak_browser("Emergency! Help needed!")

    if st.button("🚪 Logout", key="logout_btn"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ---- Main Header ----
st.markdown(f"""
<div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem;">
    <div>
        <h1>🛡️ SheSense SafeRoute AI+</h1>
        <div style="color:#8898aa; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase; margin-top:-0.3rem;">Advanced Safety Intelligence System</div>
    </div>
    <div style="text-align:right;">
        <div style="color:#8898aa; font-size:0.72rem;">EMERGENCY STATUS</div>
        <div style="font-family:'Orbitron',monospace; font-size:0.9rem;
                    color:{'#ff3b5c' if st.session_state.emergency_status != 'Normal' else '#00e676'}; font-weight:700;">
            {'🔴 ' + st.session_state.emergency_status if st.session_state.emergency_status != 'Normal' else '🟢 Normal'}
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

show_alarm_ui()

# ================================================================
# POLICE MODULES
# ================================================================
if st.session_state.user_role == "police":
    if module == "Police Dashboard":
        st.markdown('<div class="module-header"><span class="module-icon">🚔</span><h2 style="border:none!important;padding:0!important;color:#4fc3f7!important;">Police Command Center</h2></div>', unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Active Alerts", len([a for a in DB["alerts"] if a.get("recipient_type") == "Police"]))
        m2.metric("Total Incidents", len(DB["incidents"]))
        m3.metric("Network", st.session_state.network_status)
        m4.metric("Queued", len(st.session_state.queued_alerts))

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="she-card" style="border-color:rgba(79,195,247,0.3);">
                <div style="color:#4fc3f7; font-family:'Orbitron',monospace; font-size:0.8rem; letter-spacing:1px; margin-bottom:0.6rem;">STATION INFO</div>
                <div class="info-box"><div class="info-label">Station</div><div class="info-value">{st.session_state.police_station or st.session_state.police_station_name}</div></div>
                <div class="info-box"><div class="info-label">Badge ID</div><div class="info-value">{st.session_state.police_badge_id or 'N/A'}</div></div>
                <div class="info-box"><div class="info-label">Officer</div><div class="info-value">{st.session_state.user_name}</div></div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            recent_police_alerts = [a for a in DB["alerts"] if a.get("recipient_type") == "Police"][-3:]
            if recent_police_alerts:
                st.markdown('<div style="color:#4fc3f7; font-size:0.8rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">Recent SOS Alerts</div>', unsafe_allow_html=True)
                for a in reversed(recent_police_alerts):
                    st.markdown(f"""
                    <div style="background:rgba(79,195,247,0.06); border:1px solid rgba(79,195,247,0.2); border-radius:8px; padding:0.7rem; margin-bottom:0.4rem;">
                        <span style="color:#4fc3f7; font-weight:700;">{a.get('mobile_number','N/A')}</span>
                        <span style="color:#8898aa; font-size:0.75rem; float:right;">{a.get('time','')}</span><br>
                        <span style="color:#e8f0fe; font-size:0.8rem;">Risk: {a.get('risk_level','?')} | {a.get('emergency_status','?')}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No active alerts")
        st.markdown("### Live Map")
        show_map()
        voice_block("police_dash", "📡 Say 'dispatch unit' or 'acknowledge alert'")

    elif module == "Active Alerts":
        st.markdown('<div class="module-header"><span class="module-icon">🚨</span><h2 style="border:none!important;padding:0!important;color:#4fc3f7!important;">Active SOS Alerts</h2></div>', unsafe_allow_html=True)
        police_alerts = [a for a in DB["alerts"] if a.get("recipient_type") == "Police"]
        if police_alerts:
            for i, a in enumerate(reversed(police_alerts)):
                st.markdown(f"""
                <div class="she-card" style="border-color:rgba(255,59,92,0.3);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="font-family:'Orbitron',monospace; font-weight:700; color:#ff3b5c;">SOS #{i+1}</div>
                        <span class="badge badge-danger">{a.get('status','?').upper()}</span>
                    </div>
                    <div style="margin-top:0.5rem; font-size:0.85rem; line-height:1.8;">
                        📱 <b>Mobile:</b> {a.get('mobile_number','N/A')}<br>
                        📍 <b>Location:</b> {a.get('location',{}).get('lat','?')}, {a.get('location',{}).get('lon','?')}<br>
                        ⚠️ <b>Risk Level:</b> {a.get('risk_level','?')}<br>
                        🕐 <b>Time:</b> {a.get('time','?')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active alerts from users")
        voice_block("police_alerts", "📡 Say 'unit dispatched' or 'alert acknowledged'")

    elif module == "Patrol Map":
        st.markdown('<div class="module-header"><span class="module-icon">🗺️</span><h2 style="border:none!important;padding:0!important;color:#4fc3f7!important;">Patrol Zone Map — Crime Heatmap</h2></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:rgba(79,195,247,0.05); border:1px solid rgba(79,195,247,0.2); border-radius:10px; padding:0.8rem; margin-bottom:1rem; font-size:0.82rem; color:#8898aa;">
            🔴 Red zones = high crime/accident history &nbsp;|&nbsp; 🟡 Yellow = moderate &nbsp;|&nbsp; 🟢 Green = low incident zones
        </div>
        """, unsafe_allow_html=True)
        show_crime_heatmap()
        voice_block("patrol", "📡 Say 'navigate to alert location'")

    elif module == "Incident Reports":
        st.markdown('<div class="module-header"><span class="module-icon">📋</span><h2 style="border:none!important;padding:0!important;color:#4fc3f7!important;">Incident Reports</h2></div>', unsafe_allow_html=True)
        if DB["incidents"]:
            for inc in reversed(DB["incidents"]):
                st.markdown(f"""
                <div class="she-card">
                    <b style="color:#ff3b5c;">{inc.get('type','?')}</b>
                    <span style="color:#8898aa; font-size:0.75rem; float:right;">{inc.get('time','')}</span><br>
                    <span style="font-size:0.82rem;">{inc.get('notes','No notes')}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No incident reports")

    elif module == "Saved Data":
        st.markdown('<div class="module-header"><span class="module-icon">💾</span><h2 style="border:none!important;padding:0!important;">Saved Data</h2></div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Users", len(DB["users"]))
        c2.metric("Alerts", len(DB["alerts"]))
        c3.metric("Incidents", len(DB["incidents"]))
        c4.metric("Routes", len(DB["route_logs"]))
        with st.expander("👥 Users"): st.json(DB["users"])
        with st.expander("🚨 Alerts"): st.json(DB["alerts"])
        with st.expander("📋 Incidents"): st.json(DB["incidents"])
        with st.expander("🗺️ Route Logs"): st.json(DB["route_logs"])

# ================================================================
# HOSPITAL MODULES
# ================================================================
elif st.session_state.user_role == "hospital":

    if module == "Hospital Dashboard":
        st.markdown('<div class="module-header"><span class="module-icon">🏥</span><h2 style="border:none!important;padding:0!important;color:#ef5350!important;">Hospital Command Center</h2></div>', unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Emergency Calls", len([a for a in DB["alerts"] if a.get("recipient_type") == "Hospital"]))
        m2.metric("Patient", st.session_state.amb_patient_name or "None")
        m3.metric("Blood Group", st.session_state.amb_blood_group or "Unknown")
        m4.metric("Network", st.session_state.network_status)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="she-card" style="border-color:rgba(239,83,80,0.3);">
                <div style="color:#ef5350; font-family:'Orbitron',monospace; font-size:0.8rem; letter-spacing:1px; margin-bottom:0.6rem;">PATIENT INFO</div>
                <div class="info-box"><div class="info-label">Patient Name</div><div class="info-value">{st.session_state.amb_patient_name or 'N/A'}</div></div>
                <div class="info-box"><div class="info-label">Age</div><div class="info-value">{st.session_state.amb_patient_age or 'N/A'}</div></div>
                <div class="info-box"><div class="info-label">Blood Group</div><div class="info-value">{st.session_state.amb_blood_group or 'Unknown'}</div></div>
                <div class="info-box"><div class="info-label">Due Date</div><div class="info-value">{st.session_state.amb_due_date or 'N/A'}</div></div>
                <div class="info-box"><div class="info-label">Complications</div><div class="info-value">{st.session_state.amb_complications or 'None'}</div></div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            hosp_alerts = [a for a in DB["alerts"] if a.get("recipient_type") == "Hospital"][-3:]
            if hosp_alerts:
                st.markdown('<div style="color:#ef5350; font-size:0.8rem; text-transform:uppercase; margin-bottom:0.5rem;">Recent Emergency Calls</div>', unsafe_allow_html=True)
                for a in reversed(hosp_alerts):
                    st.markdown(f"""
                    <div style="background:rgba(239,83,80,0.06); border:1px solid rgba(239,83,80,0.2); border-radius:8px; padding:0.7rem; margin-bottom:0.4rem;">
                        <span style="color:#ef5350; font-weight:700;">{a.get('mobile_number','N/A')}</span>
                        <span style="color:#8898aa; font-size:0.75rem; float:right;">{a.get('time','')}</span><br>
                        <span style="color:#e8f0fe; font-size:0.8rem;">Risk: {a.get('risk_level','?')}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No emergency calls")
        show_map()
        voice_block("hosp_dash", "📡 Say 'dispatch ambulance' or 'prepare emergency room'")

    elif module == "Emergency Queue":
        st.markdown('<div class="module-header"><span class="module-icon">🚨</span><h2 style="border:none!important;padding:0!important;color:#ef5350!important;">Emergency Queue</h2></div>', unsafe_allow_html=True)
        hosp_alerts = [a for a in DB["alerts"] if a.get("recipient_type") == "Hospital"]
        if hosp_alerts:
            for i, a in enumerate(reversed(hosp_alerts)):
                st.markdown(f"""
                <div class="she-card" style="border-color:rgba(239,83,80,0.3);">
                    <div style="font-family:'Orbitron',monospace; color:#ef5350; font-weight:700;">EMERGENCY #{i+1}</div>
                    <div style="font-size:0.85rem; margin-top:0.5rem; line-height:1.8;">
                        📱 <b>Patient Mobile:</b> {a.get('mobile_number','N/A')}<br>
                        📍 <b>Location:</b> {a.get('location',{}).get('lat','?')}, {a.get('location',{}).get('lon','?')}<br>
                        ⚠️ <b>Severity:</b> {a.get('risk_level','?')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No emergency cases")

    elif module == "Ambulance Dispatch":
        st.markdown('<div class="module-header"><span class="module-icon">🚑</span><h2 style="border:none!important;padding:0!important;color:#ef5350!important;">Ambulance Dispatch</h2></div>', unsafe_allow_html=True)
        a1, a2 = st.columns(2)
        with a1:
            dispatch_location = st.text_input("📍 Dispatch To (Address or Coords)")
            dispatch_type = st.selectbox("🏷️ Emergency Type", ["General Emergency", "Pregnant / Labor", "Accident", "Cardiac", "Other"])
            eta = st.slider("⏱️ ETA (minutes)", 3, 30, 8)
            if st.button("🚑 Dispatch Ambulance"):
                speak_browser(f"Ambulance dispatched. ETA {eta} minutes to {dispatch_location or 'alert location'}.")
                st.success(f"Ambulance dispatched! ETA: {eta} minutes")
        with a2:
            st.markdown(f"""
            <div class="eta-card">
                <div class="eta-label">Estimated Arrival</div>
                <div class="eta-time">{eta} MIN</div>
                <div class="eta-label" style="margin-top:0.3rem;">{dispatch_type}</div>
            </div>
            """, unsafe_allow_html=True)
        show_map()
        voice_block("ambulance", "📡 Say 'dispatch unit' or 'ETA update'")

    elif module == "Pregnant Route Checker":
        st.markdown('<div class="module-header"><span class="module-icon">🤰</span><h2 style="border:none!important;padding:0!important;color:#ef5350!important;">Pregnant Route Safety Checker</h2></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="she-card" style="border-color:rgba(239,83,80,0.3);">
            <div style="color:#ef5350; font-family:'Orbitron',monospace; font-size:0.85rem; font-weight:700; margin-bottom:0.5rem;">
                🚑 AMBULANCE PREGNANCY MODE
            </div>
            <div style="color:#8898aa; font-size:0.82rem;">
                Before driving to the patient, check if the route is safe and fast enough for a pregnant patient.
                This mode factors in road safety, traffic, accident-prone zones, and speed bumps.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Patient details summary
        if st.session_state.amb_patient_name:
            st.markdown(f"""
            <div class="she-card" style="background:rgba(239,83,80,0.04);">
                <div style="color:#ef5350; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">Patient on Record</div>
                <div style="font-size:0.88rem; line-height:2;">
                    👩 <b>{st.session_state.amb_patient_name}</b> &nbsp;|&nbsp;
                    🎂 Age: {st.session_state.amb_patient_age} &nbsp;|&nbsp;
                    🩸 {st.session_state.amb_blood_group}<br>
                    📅 Due: {st.session_state.amb_due_date or 'N/A'} &nbsp;|&nbsp;
                    ⚕️ {st.session_state.amb_complications or 'No known complications'}
                </div>
            </div>
            """, unsafe_allow_html=True)

        rc1, rc2 = st.columns(2)
        amb_speed_bumps = rc1.checkbox("🚧 Speed Bumps on Route")
        amb_rough_road = rc2.checkbox("🪨 Rough / Pothole Road")
        amb_traffic = rc1.selectbox("🚦 Traffic Level", ["Low", "Medium", "High"])
        amb_dist = rc2.number_input("📏 Distance (km)", min_value=0.5, max_value=50.0, value=5.0)

        complications_score = 0
        if st.session_state.amb_complications:
            if any(w in st.session_state.amb_complications.lower() for w in ["diabetes", "hypertension", "preeclampsia", "bleeding"]):
                complications_score = 3
            else:
                complications_score = 1

        if st.button("🔍 Check Route Safety for Patient"):
            route_score = 0
            if amb_speed_bumps: route_score += 2
            if amb_rough_road: route_score += 3
            if amb_traffic == "High": route_score += 2
            elif amb_traffic == "Medium": route_score += 1
            route_score += complications_score

            if route_score <= 2:
                amb_safety = "✅ Safe — Proceed with normal care"
                amb_color = "#00e676"
                amb_advice = "Route is smooth and safe for the patient. Maintain steady speed."
            elif route_score <= 5:
                amb_safety = "⚠️ Moderate Risk — Extra caution needed"
                amb_color = "#ffab00"
                amb_advice = "Reduce speed on rough patches. Ensure patient is secured and stable."
            else:
                amb_safety = "🚨 High Risk — Consider alternate route"
                amb_color = "#ff3b5c"
                amb_advice = "This route may cause discomfort or harm. Use alternative road if available. Contact hospital immediately."

            st.session_state.amb_route_checked = True
            st.session_state.amb_route_safety = amb_safety

            speak_browser(f"Route assessment complete. {amb_safety}. {amb_advice}")

            st.markdown(f"""
            <div class="she-card" style="border-color:{amb_color}60; text-align:center; padding:1.5rem;">
                <div style="font-size:1.5rem; margin-bottom:0.5rem;">{amb_safety}</div>
                <div style="color:{amb_color}; font-size:0.85rem; margin-top:0.5rem;">{amb_advice}</div>
            </div>
            """, unsafe_allow_html=True)

        show_route_options()
        show_map()
        show_google_maps_route(st.session_state.latitude, st.session_state.longitude,
                               st.session_state.destination_lat, st.session_state.destination_lon)
        voice_block("amb_route", "📡 Say 'safe to proceed' or 'find alternate route'")

    elif module == "Pregnant Emergencies":
        st.markdown('<div class="module-header"><span class="module-icon">🤰</span><h2 style="border:none!important;padding:0!important;color:#ef5350!important;">Pregnant Emergency Cases</h2></div>', unsafe_allow_html=True)
        preg_incidents = [i for i in DB["incidents"] if "pregnant" in str(i).lower()]
        if preg_incidents:
            for pi in preg_incidents:
                st.markdown(f'<div class="she-card"><b>{pi.get("type","Pregnant Emergency")}</b><br><small style="color:#8898aa">{pi.get("time","")}</small><br>{pi.get("notes","")}</div>', unsafe_allow_html=True)
        else:
            st.info("No pregnant emergency cases")
        voice_block("preg_hosp", "📡 Say 'prepare maternity ward' or 'dispatch midwife unit'")

    elif module == "Saved Data":
        st.markdown('<div class="module-header"><span class="module-icon">💾</span><h2 style="border:none!important;padding:0!important;">Saved Data</h2></div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Users", len(DB["users"]))
        c2.metric("Alerts", len(DB["alerts"]))
        c3.metric("Incidents", len(DB["incidents"]))
        c4.metric("Routes", len(DB["route_logs"]))
        with st.expander("🚨 Alerts"): st.json(DB["alerts"])
        with st.expander("📋 Incidents"): st.json(DB["incidents"])

# ================================================================
# USER MODULES
# ================================================================
else:
    if module == "Dashboard":
        st.markdown('<div class="module-header"><span class="module-icon">📊</span><h2 style="border:none!important;padding:0!important;">Dashboard</h2></div>', unsafe_allow_html=True)
        left, right = st.columns([1, 1])
        with left:
            st.markdown('<div class="she-card">', unsafe_allow_html=True)
            st.markdown('<div style="color:#00f0ff; font-size:0.78rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.6rem;">📍 Location Access</div>', unsafe_allow_html=True)

            show_location_permission_request()

            if st.button("📍 Use Demo Location (Coimbatore)"):
                enable_live_location()
                speak_browser("Location enabled successfully.")
                st.success("Location enabled! Latitude: 11.0168, Longitude: 76.9558")

            st.session_state.latitude = st.number_input("Latitude", value=float(st.session_state.latitude), format="%.6f")
            st.session_state.longitude = st.number_input("Longitude", value=float(st.session_state.longitude), format="%.6f")
            maps_url = get_google_maps_url(st.session_state.latitude, st.session_state.longitude)
            st.markdown(f'<a href="{maps_url}" target="_blank" style="color:#00f0ff; font-size:0.82rem;">🗺️ View My Location on Google Maps →</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div style="color:#8898aa; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px; margin:0.8rem 0 0.4rem 0;">Emergency Contacts</div>', unsafe_allow_html=True)
            for name, num in [(st.session_state.contact_1_name, st.session_state.contact_1_number),
                               (st.session_state.contact_2_name, st.session_state.contact_2_number),
                               (st.session_state.contact_3_name, st.session_state.contact_3_number)]:
                if name:
                    initial = name[0].upper()
                    st.markdown(f"""
                    <div class="contact-card">
                        <div class="contact-avatar">{initial}</div>
                        <div><div style="font-weight:600; font-size:0.9rem;">{name}</div>
                        <div style="color:#8898aa; font-size:0.78rem;">{num}</div></div>
                    </div>
                    """, unsafe_allow_html=True)

        with right:
            m1, m2, m3 = st.columns(3)
            m1.metric("Network", st.session_state.network_status)
            m2.metric("Safety", st.session_state.route_safety)
            m3.metric("Queued Alerts", len(st.session_state.queued_alerts))

            st.markdown(f"""
            <div class="she-card" style="margin-top:0.8rem;">
                <div style="color:#8898aa; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">Status Summary</div>
                <div style="font-size:0.88rem; line-height:2;">
                    👤 <b>User:</b> {st.session_state.user_name}<br>
                    🔑 <b>Distress Word:</b> {'Set ✅' if st.session_state.distress_word else 'Not Set ❌'}<br>
                    📡 <b>Last Alert:</b> {st.session_state.last_alert_time or 'Never'}<br>
                    🎙️ <b>Last Voice:</b> {st.session_state.voice_last_message or 'None'}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Neighbor alarm quick access
            show_neighbor_alarm()

        st.markdown("### 🗺️ Live Route & Safety Map")
        show_map()
        voice_block("dashboard", "📡 Say your distress word or 'navigate home' to activate safety features")

    elif module == "Route Planning":
        st.markdown('<div class="module-header"><span class="module-icon">🗺️</span><h2 style="border:none!important;padding:0!important;">Route Planning</h2></div>', unsafe_allow_html=True)

        # Location setup
        loc_col1, loc_col2 = st.columns(2)
        with loc_col1:
            st.markdown('<div style="color:#00f0ff; font-size:0.78rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">📍 Your Current Location</div>', unsafe_allow_html=True)
            show_location_permission_request()
            st.session_state.latitude = st.number_input("Lat", value=float(st.session_state.latitude), format="%.6f", key="rp_lat")
            st.session_state.longitude = st.number_input("Lon", value=float(st.session_state.longitude), format="%.6f", key="rp_lon")

        with loc_col2:
            st.markdown('<div style="color:#00e676; font-size:0.78rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem;">🏁 Destination</div>', unsafe_allow_html=True)
            st.session_state.destination_name = st.text_input("Destination Name", value=st.session_state.destination_name, placeholder="e.g. Coimbatore Airport")
            st.session_state.destination_lat = st.number_input("Dest Lat", value=float(st.session_state.destination_lat), format="%.6f")
            st.session_state.destination_lon = st.number_input("Dest Lon", value=float(st.session_state.destination_lon), format="%.6f")

        st.markdown('<div class="she-divider"></div>', unsafe_allow_html=True)

        # Route options with crime history
        routes = show_route_options()

        # Route selection
        route_choice = st.selectbox("🔍 Select a Route",
            [f"Route {r['id']} — {r['name'].split('—')[1].strip()} ({r['safety']})" for r in routes])
        chosen_id = route_choice.split(" ")[1]  # A, B, or C
        chosen_route = next(r for r in routes if r["id"] == chosen_id)

        if st.button("✅ Confirm Route & Start Navigation"):
            st.session_state.route_safety = chosen_route["safety"]
            st.session_state.route_reason = f"Crime score: {chosen_route['crime_score']}/10 — {', '.join(chosen_route['incidents'])}"
            st.session_state.selected_route = chosen_route["name"]
            st.session_state.navigation_active = True
            st.session_state.current_step_index = 0
            log_route()
            speak_browser(f"Route {chosen_id} confirmed. Starting navigation. {chosen_route['safety']}. {chosen_route['via']}")
            st.rerun()

        # Google Maps open link
        show_google_maps_route(st.session_state.latitude, st.session_state.longitude,
                               st.session_state.destination_lat, st.session_state.destination_lon)

        # Crime heatmap
        st.markdown("### 🗺️ Crime & Safety Heatmap")
        st.markdown('<div style="color:#8898aa; font-size:0.78rem; margin-bottom:0.5rem;">Red = high crime/accident zones. Plan your route to avoid red areas.</div>', unsafe_allow_html=True)
        show_crime_heatmap()

        # Navigation
        if st.session_state.navigation_active:
            st.markdown('<div class="she-divider"></div>', unsafe_allow_html=True)
            st.markdown("### 🎙️ Turn-by-Turn Voice Navigation")
            show_navigation_steps(st.session_state.get("chosen_route_id", "B"))

        auto_alerts = voice_block("route", "📡 Say 'go by route B' to confirm or say your distress word for emergency")
        if auto_alerts:
            show_alert_dispatch(auto_alerts)

    elif module == "Safety Monitor":
        st.markdown('<div class="module-header"><span class="module-icon">🔍</span><h2 style="border:none!important;padding:0!important;">Safety Monitor</h2></div>', unsafe_allow_html=True)
        a, b = st.columns(2)
        night = a.checkbox("🌙 Night Travel", key="sm_night")
        low_light = a.checkbox("💡 Low Light Area", key="sm_low")
        isolated = b.checkbox("🏚️ Isolated Area", key="sm_iso")
        distress_text = b.text_area("📝 Distress Text / Describe Situation", placeholder="Describe what you're observing...")

        if st.button("🔎 Analyze Safety"):
            result = classify_safety(night, low_light, isolated, distress_text)
            st.session_state.route_safety = result
            speak_browser(f"Safety analysis complete. Current level: {result}.")

        if st.session_state.route_safety not in ["Unknown"]:
            colors_map = {"High Safe": ("#00e676", "✅"), "Low Safe": ("#ffab00", "⚠️"),
                          "Risky Area": ("#ff3b5c", "🔴"), "Critical Emergency": ("#ff3b5c", "🚨")}
            col_c, icon = colors_map.get(st.session_state.route_safety, ("#8898aa", "❓"))
            st.markdown(f"""
            <div class="she-card" style="border-color:{col_c}40; text-align:center; padding:1.5rem;">
                <div style="font-size:2rem;">{icon}</div>
                <div style="font-family:'Orbitron',monospace; font-size:1.1rem; color:{col_c}; font-weight:700; margin-top:0.5rem;">
                    {st.session_state.route_safety}
                </div>
            </div>
            """, unsafe_allow_html=True)

        show_neighbor_alarm()
        voice_block("safety", "📡 Say 'I feel unsafe' or your distress word for instant emergency")

    elif module == "Emergency":
        st.markdown('<div class="module-header"><span class="module-icon">🆘</span><h2 style="border:none!important;padding:0!important;">Emergency Module</h2></div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center; padding:1rem 0 0.5rem 0;">
            <div style="color:#8898aa; font-size:0.78rem; text-transform:uppercase; letter-spacing:2px; margin-bottom:0.8rem;">Tap to send emergency alerts to all contacts</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            if st.button("🆘 MANUAL SOS — EMERGENCY", key="sos_main"):
                created = trigger_emergency("Manual SOS")
                play_alarm_js(emergency=True)
                speak_browser("Emergency SOS activated! Sending alerts to your emergency contacts, police and hospital right now!")
                show_alert_dispatch(created)

        st.markdown('<div class="she-divider"></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="she-card">
                <div style="color:#8898aa; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Status</div>
                <div style="color:#{'ff3b5c' if st.session_state.emergency_status != 'Normal' else 'e8f0fe'}; font-weight:700; font-size:0.95rem; margin-top:0.3rem;">{st.session_state.emergency_status}</div>
                <div style="color:#8898aa; font-size:0.75rem; margin-top:0.5rem;">Last Alert: {st.session_state.last_alert_time or 'Never'}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="she-card">
                <div style="color:#8898aa; font-size:0.75rem; text-transform:uppercase; letter-spacing:1px;">Alert Recipients</div>
                <div style="font-size:0.82rem; margin-top:0.4rem; line-height:2;">
                    👤 {st.session_state.contact_1_name or 'Contact 1'}<br>
                    👤 {st.session_state.contact_2_name or 'Contact 2'}<br>
                    🚔 {st.session_state.police_station_name}<br>
                    🏥 {st.session_state.hospital_name}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Neighbor alarm in emergency
        st.markdown('<div class="she-divider"></div>', unsafe_allow_html=True)
        show_neighbor_alarm()

        alerts = voice_block("emergency", "📡 Say your distress word to silently trigger SOS. Or say 'call police' or 'call ambulance'")
        if alerts:
            show_alert_dispatch(alerts)

    elif module == "Offline Mode":
        st.markdown('<div class="module-header"><span class="module-icon">📡</span><h2 style="border:none!important;padding:0!important;">Offline Mode</h2></div>', unsafe_allow_html=True)

        x, y = st.columns(2)
        if x.button("📵 Simulate No Signal"):
            st.session_state.network_status = "Offline"
            speak_browser("Network offline. Alerts will be queued and sent when connection is restored.")
            st.warning("Network offline. Alerts will be queued.")
        if y.button("📶 Restore Network"):
            st.session_state.network_status = "Online"
            count = flush_queued_alerts()
            speak_browser(f"Network restored. {count} queued alerts have been sent.")
            st.success(f"Network restored. {count} queued alerts sent.")

        st.markdown(f"""
        <div class="she-card" style="text-align:center;">
            <div style="font-size:2rem;">{'📵' if st.session_state.network_status == 'Offline' else '📶'}</div>
            <div style="font-family:'Orbitron',monospace; font-weight:700; font-size:1rem; color:{'#ff3b5c' if st.session_state.network_status == 'Offline' else '#00e676'}; margin-top:0.5rem;">
                {st.session_state.network_status.upper()}
            </div>
            <div style="color:#8898aa; margin-top:0.3rem; font-size:0.85rem;">Queued Alerts: {len(st.session_state.queued_alerts)}</div>
        </div>
        """, unsafe_allow_html=True)

        # Offline practical features
        st.markdown("""
        <div class="she-card" style="border-color:rgba(255,171,0,0.3);">
            <div style="color:#ffab00; font-family:'Orbitron',monospace; font-size:0.85rem; font-weight:700; margin-bottom:0.8rem;">
                📵 OFFLINE SAFETY TOOLS — Available Without Internet
            </div>
            <div style="color:#8898aa; font-size:0.85rem; line-height:2.0;">
                🔊 <b>Neighbor Alarm</b> — Loud audio alarm (no internet needed)<br>
                📸 <b>Incident Capture</b> — Take photos/videos locally (stored on device)<br>
                🗺️ <b>Last Known Location</b> — Saved before going offline<br>
                📋 <b>Alert Queue</b> — Alerts stored and auto-sent when network returns<br>
                🎙️ <b>Offline Voice Log</b> — Record voice notes saved locally<br>
                🔑 <b>Distress Detection</b> — Keyword detection still active locally<br>
                📞 <b>Emergency Dial</b> — Direct phone call bypass (see below)
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="she-card" style="border-color:rgba(0,230,118,0.3);">
            <div style="color:#00e676; font-family:'Orbitron',monospace; font-size:0.85rem; font-weight:700; margin-bottom:0.8rem;">
                📞 DIRECT CALL — NO INTERNET REQUIRED
            </div>
            <div style="color:#8898aa; font-size:0.85rem; margin-bottom:0.8rem;">
                These actions bypass the app and directly use your phone's calling capability:
            </div>
        </div>
        """, unsafe_allow_html=True)

        oc1, oc2, oc3 = st.columns(3)
        oc1.markdown('<a href="tel:100" style="display:block; background:rgba(79,195,247,0.1); border:1px solid rgba(79,195,247,0.3); border-radius:10px; padding:0.8rem; text-align:center; color:#4fc3f7; text-decoration:none; font-weight:700;">🚔<br>Call Police<br><small>100</small></a>', unsafe_allow_html=True)
        oc2.markdown('<a href="tel:108" style="display:block; background:rgba(239,83,80,0.1); border:1px solid rgba(239,83,80,0.3); border-radius:10px; padding:0.8rem; text-align:center; color:#ef5350; text-decoration:none; font-weight:700;">🚑<br>Ambulance<br><small>108</small></a>', unsafe_allow_html=True)
        oc3.markdown('<a href="tel:112" style="display:block; background:rgba(233,30,140,0.1); border:1px solid rgba(233,30,140,0.3); border-radius:10px; padding:0.8rem; text-align:center; color:#e91e8c; text-decoration:none; font-weight:700;">🆘<br>Emergency<br><small>112</small></a>', unsafe_allow_html=True)

        st.markdown('<div style="margin-top:1rem;"></div>', unsafe_allow_html=True)
        show_neighbor_alarm()
        voice_block("offline", "📡 Offline voice commands still queue alerts for later sending")

    elif module == "Incident Recovery":
        st.markdown('<div class="module-header"><span class="module-icon">📋</span><h2 style="border:none!important;padding:0!important;">Incident Recovery</h2></div>', unsafe_allow_html=True)

        incident_type = st.selectbox("⚠️ Incident Type", ["Theft", "Attack", "Harassment", "Medical Emergency",
                                                            "Road Accident", "Eve Teasing", "Stalking", "Other"])
        notes = st.text_area("📝 Notes / Description", placeholder="Describe the incident in detail...")

        st.markdown('<div class="she-divider"></div>', unsafe_allow_html=True)

        # Media capture section
        st.markdown("### 📸 Capture Incident Evidence")
        st.markdown('<div style="color:#8898aa; font-size:0.82rem; margin-bottom:0.8rem;">Take a photo or record video as proof. Files are saved directly to your device gallery/photos.</div>', unsafe_allow_html=True)
        show_incident_media_capture()

        # Also allow uploading existing file
        st.markdown('<div class="she-divider"></div>', unsafe_allow_html=True)
        st.markdown("#### 📁 Or Upload Existing Photo/Video")
        uploaded_media = st.file_uploader("Upload incident photo or video", type=["jpg", "jpeg", "png", "mp4", "mov", "webm"])
        if uploaded_media:
            media_path = INCIDENT_MEDIA_DIR / f"{now_str().replace(' ','_').replace(':','-')}_{uploaded_media.name}"
            media_path.write_bytes(uploaded_media.read())
            if uploaded_media.type.startswith("image"):
                st.image(uploaded_media, caption="Uploaded Evidence", use_container_width=True)
            else:
                st.video(uploaded_media)
            st.session_state.incident_media_files.append(str(media_path))
            st.success(f"✅ Media saved: {media_path.name}")

        st.markdown('<div class="she-divider"></div>', unsafe_allow_html=True)

        if st.button("📄 Generate Incident Report"):
            report = {
                "type": incident_type, "notes": notes, "time": now_str(),
                "location": {"lat": st.session_state.latitude, "lon": st.session_state.longitude},
                "media_files": st.session_state.incident_media_files,
                "guidance": "Move to open area, avoid isolated route, wait near visible point."
            }
            st.session_state.incident_report = json.dumps(report, indent=2)
            log_incident(report)
            speak_browser(f"Incident report for {incident_type} has been generated and logged.")
            st.success("✅ Incident report generated and saved")

        if st.session_state.incident_report:
            st.markdown('<div class="she-card">', unsafe_allow_html=True)
            st.text_area("Report", st.session_state.incident_report, height=220)
            st.markdown('</div>', unsafe_allow_html=True)

        voice_block("incident", "📡 Say 'report incident' or describe what happened")

    elif module == "Pregnant Mode":
        st.markdown('<div class="module-header"><span class="module-icon">🤰</span><h2 style="border:none!important;padding:0!important;">Pregnant Emergency Mode</h2></div>', unsafe_allow_html=True)
        st.session_state.pregnant_mode = st.checkbox("Enable Pregnant Mode", value=st.session_state.pregnant_mode)
        if st.session_state.pregnant_mode:
            symptom = st.selectbox("🩺 Symptom", ["Normal", "Pain", "Bleeding", "Dizziness", "Critical"])
            if st.button("🔍 Check Pregnancy Emergency"):
                severity = pregnant_severity_from_symptom(symptom)
                st.session_state.pregnant_severity = severity
                if severity == "Critical":
                    st.session_state.route_safety = "Critical Emergency"
                    trigger_emergency("pregnant critical emergency", fearful=True)
                    play_alarm_js(emergency=True)
                    speak_browser("Critical pregnancy emergency detected! Ambulance dispatched. ETA 8 minutes. Stay calm and do not move.")
                    st.markdown("""
                    <div class="alert-notification emergency-pulse">
                        <div class="alert-title">🚨 CRITICAL PREGNANCY EMERGENCY</div>
                        <div class="alert-body">Ambulance dispatched • Police notified • Emergency contacts alerted</div>
                    </div>
                    """, unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    c1.markdown('<div class="eta-card"><div class="eta-label">Ambulance ETA</div><div class="eta-time">8 MIN</div><div class="eta-label">Pickup: Main road junction</div></div>', unsafe_allow_html=True)
                    c2.markdown(f'<div class="eta-card" style="background:rgba(79,195,247,0.08); border-color:rgba(79,195,247,0.3);"><div class="eta-label" style="color:#8898aa;">Nearest Hospital</div><div style="font-family:Orbitron,monospace; font-size:1.2rem; color:#4fc3f7; font-weight:900;">{st.session_state.hospital_name}</div><div class="eta-label">Emergency & Trauma</div></div>', unsafe_allow_html=True)
                elif severity == "High Risk":
                    speak_browser("High risk pregnancy condition detected. Please seek medical attention immediately.")
                    st.warning("⚠️ High Risk pregnancy condition — seek immediate medical attention")
                else:
                    speak_browser("Condition appears normal. Stay calm and monitor symptoms.")
                    st.success("✅ Normal condition")

            severity_badge = "badge-danger" if st.session_state.pregnant_severity == "Critical" else \
                             "badge-warn" if st.session_state.pregnant_severity == "High Risk" else "badge-safe"
            st.markdown(f'<div style="margin:0.5rem 0;"><span class="badge {severity_badge}">Severity: {st.session_state.pregnant_severity}</span></div>', unsafe_allow_html=True)
            show_map()
            show_google_maps_route(st.session_state.latitude, st.session_state.longitude,
                                   st.session_state.destination_lat, st.session_state.destination_lon)
        voice_block("pregnant", "📡 Say 'I need ambulance' or 'emergency labor' to dispatch help immediately")

    elif module == "Police Assistance":
        st.markdown('<div class="module-header"><span class="module-icon">🚔</span><h2 style="border:none!important;padding:0!important;">Police Assistance</h2></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="she-card" style="border-color:rgba(79,195,247,0.3);">
            <div class="info-box"><div class="info-label">Station</div><div class="info-value">{st.session_state.police_station_name}</div></div>
            <div class="info-box"><div class="info-label">Division</div><div class="info-value">{st.session_state.police_station_branch}</div></div>
            <div class="info-box"><div class="info-label">Address</div><div class="info-value">{st.session_state.police_station_address}</div></div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚔 Send Police Alert Now"):
            created = send_or_queue_alerts("police assistance")
            play_alarm_js(emergency=True)
            speak_browser("Police alert sent. Help is on the way.")
            show_alert_dispatch([a for a in created if a["recipient_type"] == "Police"])

        st.markdown('<a href="tel:100" style="display:inline-block; margin-top:0.5rem; padding:0.5rem 1.2rem; background:rgba(79,195,247,0.1); border:1px solid rgba(79,195,247,0.3); border-radius:8px; color:#4fc3f7; text-decoration:none; font-weight:700; font-size:0.85rem;">📞 Direct Call Police — 100</a>', unsafe_allow_html=True)
        voice_block("police", "📡 Say 'call police' or 'send police alert' to notify authorities")

    elif module == "Hospital Assistance":
        st.markdown('<div class="module-header"><span class="module-icon">🏥</span><h2 style="border:none!important;padding:0!important;">Hospital Assistance</h2></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="she-card" style="border-color:rgba(239,83,80,0.3);">
            <div class="info-box"><div class="info-label">Hospital</div><div class="info-value">{st.session_state.hospital_name}</div></div>
            <div class="info-box"><div class="info-label">Department</div><div class="info-value">{st.session_state.hospital_branch}</div></div>
            <div class="info-box"><div class="info-label">Address</div><div class="info-value">{st.session_state.hospital_address}</div></div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🏥 Send Hospital / Ambulance Alert"):
            created = send_or_queue_alerts("hospital assistance")
            play_alarm_js(emergency=True)
            speak_browser("Hospital and ambulance alert sent. Emergency team is responding.")
            show_alert_dispatch([a for a in created if a["recipient_type"] == "Hospital"])

        st.markdown('<a href="tel:108" style="display:inline-block; margin-top:0.5rem; padding:0.5rem 1.2rem; background:rgba(239,83,80,0.1); border:1px solid rgba(239,83,80,0.3); border-radius:8px; color:#ef5350; text-decoration:none; font-weight:700; font-size:0.85rem;">📞 Direct Call Ambulance — 108</a>', unsafe_allow_html=True)
        voice_block("hospital", "📡 Say 'call ambulance' or 'I need medical help' to dispatch emergency services")

    elif module == "Camera Light Detection":
        st.markdown('<div class="module-header"><span class="module-icon">📷</span><h2 style="border:none!important;padding:0!important;">Camera Light Detection</h2></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="she-card" style="border-color:rgba(0,240,255,0.3);">
            <div style="color:#00f0ff; font-family:'Orbitron',monospace; font-size:0.85rem; font-weight:700; margin-bottom:0.5rem;">
                💡 LIVE AMBIENT LIGHT DETECTION
            </div>
            <div style="color:#8898aa; font-size:0.82rem; line-height:1.8;">
                This module uses your device's <b>rear camera</b> to detect light levels on your route in real-time.
                No image is uploaded or stored — all analysis happens locally in your browser.<br>
                Low light areas are a key risk factor for harassment and theft.
            </div>
        </div>
        """, unsafe_allow_html=True)

        show_camera_light_detection()

        st.markdown("""
        <div style="background:rgba(255,171,0,0.06); border:1px solid rgba(255,171,0,0.2); border-radius:10px; padding:0.8rem; margin-top:0.8rem; font-size:0.82rem;">
            <span style="color:#ffab00; font-weight:700;">📌 How to use:</span>
            <span style="color:#8898aa;"> Point your phone camera toward the path ahead of you while walking.
            The app will continuously analyze brightness and alert you to dark/risky zones.
            🌑 Dark areas → Risky &nbsp;|&nbsp; 🌤️ Moderate → Caution &nbsp;|&nbsp; ☀️ Bright → Safe</span>
        </div>
        """, unsafe_allow_html=True)

        voice_block("light", "📡 Camera light detection active. You'll be warned about dark zones automatically.")

    elif module == "Saved Data":
        st.markdown('<div class="module-header"><span class="module-icon">💾</span><h2 style="border:none!important;padding:0!important;">Saved Data</h2></div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Users", len(DB["users"]))
        c2.metric("Alerts", len(DB["alerts"]))
        c3.metric("Incidents", len(DB["incidents"]))
        c4.metric("Routes", len(DB["route_logs"]))
        with st.expander("👥 Users"): st.json(DB["users"])
        with st.expander("🚨 Alerts"): st.json(DB["alerts"])
        with st.expander("📋 Incidents"): st.json(DB["incidents"])
        with st.expander("🗺️ Route Logs"): st.json(DB["route_logs"])
        with st.expander("🚔 Police Users"): st.json(DB.get("police_users", []))
        with st.expander("🏥 Hospital Users"): st.json(DB.get("hospital_users", []))