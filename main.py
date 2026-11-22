"""
Cyber Incident Investigation Dashboard
Main Streamlit application entry point.
Redesigned with Modern Dark (Charcoal & Peach/Coral) theme.
"""

import streamlit as st
import pandas as pd
import re

# -- Page config must be first --
st.set_page_config(
    page_title="Cyber Incident Investigation Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

from database import create_connection
import queries as q

# ══════════════════════════════════════════════════════════════
#  CSS – Modern Dark (Charcoal & Muted Peach/Coral) Theme
#  Palette:
#   Main background:    #17191D
#   Sidebar background: #1D2025
#   Card background:    #24262B
#   Elevated surfaces:  #2B2D32
#   Primary accent:     #E99B83 (Peach/Coral)
#   Primary text:       #F4F1EF
#   Secondary text:     #A5A5AA
#   Muted text:         #777A82
#   Borders:            #35373D
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Global View Containers ── */
[data-testid="stAppViewContainer"] {
    background-color: #17191D !important;
    color: #F4F1EF !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
[data-testid="stHeader"] {
    background-color: rgba(23, 25, 29, 0.85) !important;
    backdrop-filter: blur(8px);
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* ── Sidebar Styling ── */
[data-testid="stSidebar"] {
    background-color: #1D2025 !important;
    border-right: 1px solid #35373D !important;
}
[data-testid="stSidebar"] * {
    color: #A5A5AA;
}
[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 4px;
}
[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: transparent;
    padding: 9px 14px;
    border-radius: 6px;
    margin-bottom: 2px;
    color: #A5A5AA !important;
    font-size: 0.88rem;
    font-weight: 500;
    border-left: 3px solid transparent;
    transition: all 0.15s ease-in-out;
    cursor: pointer;
}
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: #24262B;
    color: #F4F1EF !important;
}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: #24262B;
    color: #E99B83 !important;
    border-left: 3px solid #E99B83;
    font-weight: 600;
}
[data-testid="stSidebar"] div[role="radiogroup"] input {
    display: none;
}

/* ── Typography & Headings ── */
h1, h2, h3, h4, h5, h6 {
    color: #F4F1EF !important;
    font-weight: 600 !important;
    letter-spacing: -0.015em;
}
p, span, li, label, .stMarkdown {
    color: #A5A5AA;
}
strong, b {
    color: #F4F1EF !important;
}
hr {
    border: none !important;
    border-top: 1px solid #35373D !important;
    margin: 20px 0 !important;
}

.page-title {
    font-size: 1.85rem;
    font-weight: 700;
    color: #F4F1EF !important;
    letter-spacing: -0.02em;
    margin-bottom: 4px;
}
.page-subtitle {
    font-size: 0.88rem;
    color: #A5A5AA;
    margin-bottom: 22px;
    line-height: 1.5;
}
.section-header-box {
    display: flex;
    align-items: center;
    gap: 10px;
    border-left: 3px solid #E99B83;
    padding-left: 12px;
    margin-top: 24px;
    margin-bottom: 14px;
}
.section-header-box h3 {
    margin: 0;
    font-size: 1.15rem;
    color: #F4F1EF !important;
}

/* ── Modern KPI Cards ── */
.kpi-card {
    background: #24262B;
    border: 1px solid #35373D;
    border-radius: 10px;
    padding: 18px 18px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s ease, transform 0.2s ease;
    margin-bottom: 10px;
}
.kpi-card:hover {
    border-color: #E99B83;
}
.kpi-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 3px;
    height: 100%;
    background: #35373D;
}
.kpi-card.kpi-accent::before   { background: #E99B83; }
.kpi-card.kpi-critical::before { background: #E06C75; }
.kpi-card.kpi-high::before     { background: #E58E3C; }
.kpi-card.kpi-resolved::before { background: #6BAE75; }
.kpi-card.kpi-open::before     { background: #E58E3C; }
.kpi-card.kpi-alerts::before   { background: #D4A359; }

.kpi-card .kpi-label {
    font-size: 0.74rem;
    color: #777A82;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
    margin-bottom: 8px;
}
.kpi-card .kpi-value {
    font-size: 2.1rem;
    font-weight: 700;
    line-height: 1.1;
    color: #F4F1EF;
}
.kpi-card.kpi-accent .kpi-value   { color: #E99B83; }
.kpi-card.kpi-critical .kpi-value { color: #E06C75; }
.kpi-card.kpi-high .kpi-value     { color: #E58E3C; }
.kpi-card.kpi-resolved .kpi-value { color: #6BAE75; }
.kpi-card.kpi-open .kpi-value     { color: #E58E3C; }
.kpi-card.kpi-alerts .kpi-value   { color: #D4A359; }

/* ── Tabs Navigation ── */
[data-baseweb="tab-list"] {
    background-color: #1D2025 !important;
    border-bottom: 1px solid #35373D !important;
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
}
[data-baseweb="tab"] {
    color: #A5A5AA !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    padding: 8px 18px !important;
    border: none !important;
    background: transparent !important;
}
[data-baseweb="tab"]:hover {
    color: #F4F1EF !important;
    background: #24262B !important;
}
[data-baseweb="tab"][aria-selected="true"] {
    color: #E99B83 !important;
    background: #24262B !important;
    font-weight: 600 !important;
    border-bottom: 2px solid #E99B83 !important;
}

/* ── Form Inputs & Selectboxes ── */
div[data-baseweb="input"] {
    background-color: #24262B !important;
    border: 1px solid #35373D !important;
    border-radius: 6px !important;
}
div[data-baseweb="input"] input {
    color: #F4F1EF !important;
    font-size: 0.9rem !important;
}
div[data-baseweb="input"]:focus-within {
    border-color: #E99B83 !important;
    box-shadow: 0 0 0 1px #E99B83 !important;
}
div[data-baseweb="select"] > div {
    background-color: #24262B !important;
    border: 1px solid #35373D !important;
    border-radius: 6px !important;
    color: #F4F1EF !important;
}
div[data-baseweb="select"]:focus-within > div {
    border-color: #E99B83 !important;
    box-shadow: 0 0 0 1px #E99B83 !important;
}
div[data-baseweb="textarea"] {
    background-color: #24262B !important;
    border: 1px solid #35373D !important;
    border-radius: 6px !important;
}
div[data-baseweb="textarea"] textarea {
    color: #F4F1EF !important;
    font-size: 0.9rem !important;
}
div[data-baseweb="textarea"]:focus-within {
    border-color: #E99B83 !important;
    box-shadow: 0 0 0 1px #E99B83 !important;
}
input::placeholder, textarea::placeholder {
    color: #777A82 !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #F4F1EF !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

/* ── Dropdown Menu Styling ── */
ul[data-baseweb="menu"] {
    background-color: #24262B !important;
    border: 1px solid #35373D !important;
    border-radius: 6px !important;
}
li[data-baseweb="menu-item"] {
    color: #F4F1EF !important;
}
li[data-baseweb="menu-item"]:hover {
    background-color: #2B2D32 !important;
    color: #E99B83 !important;
}

/* ── Buttons ── */
.stButton > button {
    background-color: #24262B !important;
    color: #F4F1EF !important;
    border: 1px solid #35373D !important;
    border-radius: 6px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 6px 16px !important;
    transition: all 0.15s ease-in-out !important;
}
.stButton > button:hover {
    background-color: #2B2D32 !important;
    border-color: #E99B83 !important;
    color: #E99B83 !important;
}
[data-testid="stFormSubmitButton"] > button {
    background-color: #E99B83 !important;
    color: #17191D !important;
    border: none !important;
    border-radius: 6px !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    padding: 8px 22px !important;
    transition: all 0.15s ease-in-out !important;
}
[data-testid="stFormSubmitButton"] > button:hover {
    background-color: #f0ab96 !important;
    color: #17191D !important;
}
[data-testid="stDownloadButton"] > button {
    background-color: #24262B !important;
    color: #E99B83 !important;
    border: 1px solid #35373D !important;
    border-radius: 6px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background-color: #2B2D32 !important;
    border-color: #E99B83 !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    background-color: #24262B !important;
    border: 1px solid #35373D !important;
    border-radius: 8px !important;
    margin-bottom: 12px !important;
}
[data-testid="stExpander"] summary {
    color: #F4F1EF !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
}
[data-testid="stExpander"] summary:hover {
    color: #E99B83 !important;
}

/* ── Dataframes ── */
[data-testid="stDataFrame"] {
    background-color: #24262B !important;
    border: 1px solid #35373D !important;
    border-radius: 8px !important;
    padding: 2px !important;
}

/* ── Alerts ── */
div[data-testid="stAlert"] {
    background-color: #24262B !important;
    border: 1px solid #35373D !important;
    border-radius: 8px !important;
    color: #F4F1EF !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  Theme Helpers & Color Constants
# ══════════════════════════════════════════════════════════════

SEV_COLORS = {
    "Critical":   "#E06C75",  # Muted Red
    "High":       "#E58E3C",  # Muted Orange
    "Medium":     "#E5C07B",  # Muted Yellow
    "Low":        "#6BAE75",  # Muted Green
    "Unassigned": "#777A82",  # Muted Gray
}

STATUS_COLORS = {
    "Open":                "#E58E3C",
    "Under Investigation": "#E5C07B",
    "Resolved":            "#6BAE75",
    "Closed":              "#777A82",
    "Pending Assessment":  "#E99B83",
}

THEME_PEACH = "#E99B83"
THEME_AMBER = "#D4A359"
THEME_SLATE = "#5C6370"


def kpi_card(value, label, style="kpi-accent"):
    return f"""
    <div class="kpi-card {style}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """


def section_header(title):
    st.markdown(
        f"""
        <div class="section-header-box">
            <h3>{title}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )


def check_connection():
    conn = create_connection()
    if conn:
        conn.close()
        return True
    return False


def df_to_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


# ══════════════════════════════════════════════════════════════
#  Sidebar Navigation
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;padding:8px 4px 16px 4px;">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#E99B83" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            <path d="M12 8v4"/>
            <path d="M12 16h.01"/>
        </svg>
        <div>
            <div style="font-size:1.02rem;font-weight:700;color:#F4F1EF;letter-spacing:0.02em;line-height:1.2;">CYBER SHIELD</div>
            <div style="font-size:0.7rem;color:#777A82;text-transform:uppercase;letter-spacing:0.08em;font-weight:600;">Incident Investigation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid #35373D;margin:4px 0 14px 0;'>", unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "Dashboard Overview",
            "Incident Investigation",
            "Security Alerts",
            "Evidence Tracking",
            "Investigation Activities",
            "Data Entry / Record Management",
            "Analytical Insights",
            "Reports & Export",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border:none;border-top:1px solid #35373D;margin:16px 0;'>", unsafe_allow_html=True)

    # Database Status Indicator Pill
    if check_connection():
        st.markdown("""
        <div style="background:#24262B;border:1px solid #35373D;border-radius:6px;padding:9px 12px;display:flex;align-items:center;justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#6BAE75;"></span>
                <span style="font-size:0.78rem;color:#F4F1EF;font-weight:500;">MySQL Database</span>
            </div>
            <span style="font-size:0.68rem;color:#6BAE75;background:#1C2620;padding:2px 7px;border-radius:4px;font-weight:600;border:1px solid #2C4D38;">ONLINE</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:#24262B;border:1px solid #35373D;border-radius:6px;padding:9px 12px;display:flex;align-items:center;justify-content:space-between;">
            <div style="display:flex;align-items:center;gap:8px;">
                <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#E06C75;"></span>
                <span style="font-size:0.78rem;color:#F4F1EF;font-weight:500;">MySQL Database</span>
            </div>
            <span style="font-size:0.68rem;color:#E06C75;background:#2B1D20;padding:2px 7px;border-radius:4px;font-weight:600;border:1px solid #5C2B32;">OFFLINE</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:22px;padding:4px;font-size:0.72rem;color:#777A82;text-align:center;line-height:1.5;">
        Modern Dark SOC Architecture<br>MySQL Relational Engine
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PAGE 1 – Dashboard Overview
# ══════════════════════════════════════════════════════════════

def page_overview():
    st.markdown("<div class='page-title'>Dashboard Overview</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Real-time cybersecurity incident posture, alert distribution, and threat velocity</div>", unsafe_allow_html=True)

    stats = q.get_kpi_stats()
    total_alerts = q.get_total_alerts()

    # ── KPI Cards ──
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(kpi_card(stats.get("total", 0), "Total Incidents", "kpi-accent"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card(stats.get("open", 0), "Open Incidents", "kpi-open"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card(stats.get("resolved", 0), "Resolved", "kpi-resolved"), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card(stats.get("critical", 0), "Critical", "kpi-critical"), unsafe_allow_html=True)
    with c5:
        st.markdown(kpi_card(stats.get("high", 0), "High Severity", "kpi-high"), unsafe_allow_html=True)
    with c6:
        st.markdown(kpi_card(total_alerts, "Total Alerts", "kpi-alerts"), unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── Charts Row 1 ──
    col_a, col_b = st.columns(2)

    with col_a:
        section_header("Incidents by Severity")
        df_sev = q.get_incidents_by_severity()
        if not df_sev.empty:
            df_sev = df_sev.set_index("severity")
            st.bar_chart(df_sev["count"], color=THEME_PEACH)
        else:
            st.info("No incident severity data available.")

    with col_b:
        section_header("Incidents by Status")
        df_st = q.get_incidents_by_status()
        if not df_st.empty:
            df_st = df_st.set_index("status")
            st.bar_chart(df_st["count"], color=THEME_AMBER)
        else:
            st.info("No incident status data available.")

    # ── Charts Row 2 ──
    col_c, col_d = st.columns(2)

    with col_c:
        section_header("Incidents by Attack Type")
        df_type = q.get_incidents_by_type()
        if not df_type.empty:
            df_type = df_type.set_index("incident_type")
            st.bar_chart(df_type["count"], color=THEME_PEACH)
        else:
            st.info("No attack type data available.")

    with col_d:
        section_header("Alerts by Type")
        df_alert = q.get_alerts_by_type()
        if not df_alert.empty:
            df_alert = df_alert.set_index("alert_type")
            st.bar_chart(df_alert["count"], color=THEME_AMBER)
        else:
            st.info("No alert category data available.")

    # ── Trend Chart ──
    section_header("Incident Trend Over Time")
    df_trend = q.get_incident_trend()
    if not df_trend.empty:
        df_trend["date"] = pd.to_datetime(df_trend["date"])
        df_trend = df_trend.set_index("date")
        st.line_chart(df_trend["count"], color=THEME_PEACH)
    else:
        st.info("No trend data available.")

    # ── Recent Incidents Table ──
    section_header("Recent Incidents")
    df_inc = q.get_all_incidents()
    if not df_inc.empty:
        display_cols = ["incident_id", "incident_type", "severity", "status", "affected_user", "device_name", "reported_at"]
        st.dataframe(df_inc[display_cols].head(10), use_container_width=True, hide_index=True)
    else:
        st.info("No incidents found.")


# ══════════════════════════════════════════════════════════════
#  Reusable Reporter Form Component
# ══════════════════════════════════════════════════════════════

def render_incident_reporting_form(form_key_suffix=""):
    st.markdown(
        """
        <div style="background:#24262B;border:1px solid #35373D;border-left:3px solid #E99B83;border-radius:6px;padding:12px 16px;margin-bottom:18px;color:#A5A5AA;font-size:0.88rem;line-height:1.5;">
            <b>Reporter Guidance:</b> You do not need to identify the technical attack type or severity level. Describe what occurred in plain language. A security investigator will review and classify your submission.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form(f"new_incident_form_{form_key_suffix}"):
        st.markdown("**Affected User Information**")
        uc1, uc2, uc3 = st.columns(3)
        with uc1:
            ni_user_name = st.text_input("Full Name *", placeholder="e.g. Rahul Sharma", key=f"ni_uname_{form_key_suffix}")
        with uc2:
            ni_user_email = st.text_input("Email Address *", placeholder="e.g. rahul@company.com", key=f"ni_uemail_{form_key_suffix}")
        with uc3:
            ni_user_dept = st.text_input("Department *", placeholder="e.g. Finance", key=f"ni_udept_{form_key_suffix}")

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("**Affected Device Details**")
        dc1, dc2, dc3 = st.columns(3)
        with dc1:
            ni_device_name = st.text_input("Device Name *", placeholder="e.g. Rahul-Laptop", key=f"ni_dname_{form_key_suffix}")
        with dc2:
            ni_device_type = st.selectbox(
                "Device Type",
                ["Laptop", "Desktop", "Mobile", "Server", "Workstation", "Tablet", "Other"],
                key=f"ni_dtype_{form_key_suffix}",
            )
        with dc3:
            ni_device_os = st.text_input("Operating System *", placeholder="e.g. Windows 11", key=f"ni_dos_{form_key_suffix}")

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("**Incident Description**")
        ni_description = st.text_area(
            "What occurred? *",
            placeholder=(
                "Describe in detail what you saw or experienced.\n"
                "Examples:\n"
                "- Received a suspicious email requesting credential verification.\n"
                "- Device exhibited unusual outbound network traffic or unexpected popup windows.\n"
                "- Files on desktop were encrypted or renamed."
            ),
            height=130,
            key=f"ni_desc_{form_key_suffix}",
        )

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("**Suspicious IP Address** *(optional)*")
        st.caption("Provide an associated IP address if observed in firewall or connection error logs.")
        ip1, ip2, ip3 = st.columns(3)
        with ip1:
            ni_ip = st.text_input("IP Address", placeholder="e.g. 45.33.32.156", key=f"ni_ip_{form_key_suffix}")
        with ip2:
            ni_ip_type = st.selectbox("IP Type", ["External", "Internal"], key=f"ni_iptype_{form_key_suffix}")
        with ip3:
            ni_ip_loc = st.text_input("Location", placeholder="e.g. United States", key=f"ni_iploc_{form_key_suffix}")

        submitted = st.form_submit_button("Submit Incident Report")

    if submitted:
        errors = []
        if not ni_user_name.strip():
            errors.append("Full name is required.")
        if not ni_user_email.strip():
            errors.append("Email address is required.")
        elif "@" not in ni_user_email or "." not in ni_user_email.split("@")[-1]:
            errors.append("Email address does not look valid.")
        if not ni_user_dept.strip():
            errors.append("Department is required.")
        if not ni_device_name.strip():
            errors.append("Device name is required.")
        if not ni_device_os.strip():
            errors.append("Operating system is required.")
        if not ni_description.strip():
            errors.append("Incident description is required.")
        if ni_ip.strip():
            ip_pattern = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$|^([0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{0,4}$")
            if not ip_pattern.match(ni_ip.strip()):
                errors.append("IP address format is not valid (e.g. 192.168.1.10).")

        if errors:
            for e in errors:
                st.error(e)
        else:
            with st.spinner("Submitting incident report..."):
                ok, msg, detail = q.create_incident_full(
                    user_name=ni_user_name.strip(),
                    user_email=ni_user_email.strip().lower(),
                    user_department=ni_user_dept.strip(),
                    device_name=ni_device_name.strip(),
                    device_type=ni_device_type,
                    operating_system=ni_device_os.strip(),
                    description=ni_description.strip(),
                    ip_address=ni_ip.strip() if ni_ip.strip() else None,
                    ip_type=ni_ip_type,
                    ip_location=ni_ip_loc.strip() if ni_ip_loc.strip() else None,
                )

            if ok:
                st.success(f"{msg} A security investigator will review and classify your report.")
                if detail:
                    with st.expander("Submission Transaction Details"):
                        for k, v in detail.items():
                            st.markdown(f"- **{k.capitalize()}:** {v}")
                st.rerun()
            else:
                st.error(f"Failed to submit report: {msg}")


# ══════════════════════════════════════════════════════════════
#  PAGE 2 – Incident Investigation
# ══════════════════════════════════════════════════════════════

def page_incidents():
    st.markdown("<div class='page-title'>Incident Investigation</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Search, filter, examine evidence trails, and conduct investigator classification workflows</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["All Incidents", "Incident Details", "Report a Security Incident"])

    # ── Tab 1: Filter + Table ──
    with tab1:
        st.markdown("**Search & Filter Parameters**")
        fc1, fc2, fc3, fc4, fc5 = st.columns(5)
        with fc1:
            sev_filter = st.selectbox("Severity", ["All", "Critical", "High", "Medium", "Low", "Unassigned"], key="inc_sev")
        with fc2:
            stat_filter = st.selectbox("Status", ["All", "Pending Assessment", "Open", "Under Investigation", "Resolved", "Closed"], key="inc_stat")
        with fc3:
            types = ["All"] + q.get_distinct_incident_types()
            type_filter = st.selectbox("Attack Type", types, key="inc_type")
        with fc4:
            date_from = st.date_input("From Date", value=None, key="inc_dfrom")
        with fc5:
            date_to = st.date_input("To Date", value=None, key="inc_dto")

        df = q.get_all_incidents(
            severity=sev_filter,
            status=stat_filter,
            incident_type=type_filter,
            date_from=date_from,
            date_to=date_to,
        )

        if not df.empty:
            search = st.text_input("Filter results by keyword...", key="inc_search")
            if search:
                mask = df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)
                df = df[mask]

            st.markdown(f"**{len(df)} matching incident record(s)**")
            st.dataframe(df, use_container_width=True, hide_index=True)

            st.download_button(
                "Export Filtered CSV",
                data=df_to_csv(df),
                file_name="incidents.csv",
                mime="text/csv",
            )
        else:
            st.info("No incidents match the selected filters.")

    # ── Tab 2: Incident Detail View + Investigator Assessment ──
    with tab2:
        df_all = q.get_all_incidents()
        if df_all.empty:
            st.info("No incidents found in the database.")
        else:
            incident_options = {
                f"#{row['incident_id']} - {row['incident_type']} [{row['severity']}]": row["incident_id"]
                for _, row in df_all.iterrows()
            }
            selected_label = st.selectbox("Select Incident to Inspect", list(incident_options.keys()), key="inc_detail_sel")
            incident_id = incident_options[selected_label]

            detail_df = q.get_incident_detail(incident_id)
            if not detail_df.empty:
                d = detail_df.iloc[0]

                sev_color = SEV_COLORS.get(str(d.get("severity", "")), "#777A82")
                st_color  = STATUS_COLORS.get(str(d.get("status", "")), "#777A82")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div style="background:#24262B;border:1px solid #35373D;border-radius:8px;padding:18px;margin-bottom:14px;">
                        <div style="font-size:1.1rem;font-weight:600;color:#F4F1EF;margin-bottom:12px;">Incident #{d['incident_id']} &mdash; {d['incident_type']}</div>
                        <div style="display:flex;gap:10px;margin-bottom:14px;">
                            <div style="background:#2B2D32;border:1px solid #35373D;padding:4px 10px;border-radius:4px;font-size:0.8rem;color:{sev_color};font-weight:600;">Severity: {d['severity']}</div>
                            <div style="background:#2B2D32;border:1px solid #35373D;padding:4px 10px;border-radius:4px;font-size:0.8rem;color:{st_color};font-weight:600;">Status: {d['status']}</div>
                        </div>
                        <div style="font-size:0.82rem;color:#A5A5AA;margin-bottom:4px;"><b>Reported At:</b> {d['reported_at']}</div>
                        <div style="font-size:0.82rem;color:#A5A5AA;margin-bottom:12px;"><b>Incident Age:</b> {d.get('incident_age_days', 'N/A')} day(s)</div>
                        <div style="font-size:0.75rem;color:#777A82;text-transform:uppercase;font-weight:600;margin-bottom:6px;letter-spacing:0.04em;">Reported Description</div>
                        <div style="font-size:0.88rem;color:#F4F1EF;background:#1D2025;border:1px solid #35373D;border-radius:6px;padding:12px;line-height:1.5;">{d.get('description', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"""
                    <div style="background:#24262B;border:1px solid #35373D;border-radius:8px;padding:18px;margin-bottom:14px;">
                        <div style="font-size:0.92rem;font-weight:600;color:#E99B83;margin-bottom:10px;letter-spacing:0.04em;">AFFECTED ENTITY</div>
                        <div style="font-size:0.85rem;color:#F4F1EF;margin-bottom:4px;"><b>User:</b> {d.get('affected_user', 'N/A')}</div>
                        <div style="font-size:0.85rem;color:#A5A5AA;margin-bottom:4px;"><b>Email:</b> {d.get('user_email', 'N/A')}</div>
                        <div style="font-size:0.85rem;color:#A5A5AA;margin-bottom:12px;"><b>Department:</b> {d.get('department', 'N/A')}</div>
                        <div style="font-size:0.85rem;color:#F4F1EF;margin-bottom:4px;"><b>Device:</b> {d.get('device_name', 'N/A')} ({d.get('device_type', '')})</div>
                        <div style="font-size:0.85rem;color:#A5A5AA;margin-bottom:16px;"><b>OS:</b> {d.get('operating_system', 'N/A')}</div>
                        <div style="border-top:1px solid #35373D;padding-top:12px;">
                            <div style="font-size:0.92rem;font-weight:600;color:#E99B83;margin-bottom:8px;letter-spacing:0.04em;">ASSIGNED INVESTIGATOR</div>
                            <div style="font-size:0.85rem;color:#F4F1EF;margin-bottom:4px;"><b>Name:</b> {d.get('investigator', 'Unassigned')}</div>
                            <div style="font-size:0.85rem;color:#A5A5AA;margin-bottom:4px;"><b>Email:</b> {d.get('investigator_email', 'N/A')}</div>
                            <div style="font-size:0.85rem;color:#A5A5AA;"><b>Role:</b> {d.get('investigator_role', 'N/A')}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<hr>", unsafe_allow_html=True)

                # Associated Alerts
                alerts_df = q.get_incident_alerts(incident_id)
                if not alerts_df.empty:
                    section_header("Associated Alerts")
                    st.dataframe(alerts_df, use_container_width=True, hide_index=True)

                # Status History
                hist_df = q.get_incident_status_history(incident_id)
                if not hist_df.empty:
                    section_header("Status Transition History")
                    st.dataframe(hist_df, use_container_width=True, hide_index=True)

                st.markdown("<hr>", unsafe_allow_html=True)

                # ── Investigator Assessment Panel ──
                is_pending = str(d.get("status", "")) == "Pending Assessment"
                panel_label = "Investigator Assessment & Classification" if is_pending else "Update Incident Classification"
                if is_pending:
                    st.markdown(
                        """
                        <div style="background:#24262B;border:1px solid #35373D;border-left:3px solid #E5C07B;border-radius:6px;padding:12px 16px;margin-bottom:14px;font-size:0.86rem;color:#A5A5AA;">
                            <b>Pending Investigator Review:</b> This incident report was filed by an end user and requires formal threat classification, severity determination, and assignment.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with st.expander(panel_label, expanded=is_pending):
                    inv_df = q.get_all_investigators()
                    if inv_df.empty:
                        st.warning("No investigators registered in the database.")
                    else:
                        inv_map = {f"{r['name']} ({r['role']})": r["investigator_id"] for _, r in inv_df.iterrows()}

                        with st.form(f"assess_form_{incident_id}"):
                            st.markdown("**Threat Classification**")
                            ac1, ac2 = st.columns(2)
                            with ac1:
                                current_type = str(d.get("incident_type", ""))
                                default_type = "" if current_type == "Pending Classification" else current_type
                                assessed_type = st.text_input(
                                    "Incident / Attack Type *",
                                    value=default_type,
                                    placeholder="e.g. Phishing Attack, Ransomware Infection",
                                    key=f"atype_{incident_id}",
                                )
                            with ac2:
                                current_sev = str(d.get("severity", "Unassigned"))
                                sev_opts = ["Unassigned", "Low", "Medium", "High", "Critical"]
                                sev_idx = sev_opts.index(current_sev) if current_sev in sev_opts else 0
                                assessed_sev = st.selectbox(
                                    "Assessed Severity *",
                                    sev_opts,
                                    index=sev_idx,
                                    key=f"asev_{incident_id}",
                                )

                            st.markdown("**Assignment & Status Update**")
                            ic1, ic2 = st.columns(2)
                            with ic1:
                                current_stat = str(d.get("status", "Pending Assessment"))
                                stat_opts = ["Pending Assessment", "Open", "Under Investigation", "Resolved", "Closed"]
                                stat_idx = stat_opts.index(current_stat) if current_stat in stat_opts else 0
                                assessed_status = st.selectbox(
                                    "Updated Lifecycle Status *",
                                    stat_opts,
                                    index=stat_idx,
                                    key=f"astat_{incident_id}",
                                )
                            with ic2:
                                current_inv = str(d.get("investigator", ""))
                                inv_names = list(inv_map.keys())
                                current_inv_idx = next(
                                    (i for i, k in enumerate(inv_names) if k.startswith(current_inv)),
                                    0,
                                )
                                assessed_inv = st.selectbox(
                                    "Lead Investigator *",
                                    inv_names,
                                    index=current_inv_idx,
                                    key=f"ainv_{incident_id}",
                                )

                            assessment_notes = st.text_area(
                                "Assessment Notes / Action Rationale",
                                placeholder="Detail investigation findings, scope, or next mitigation steps...",
                                height=90,
                                key=f"anotes_{incident_id}",
                            )

                            assess_submitted = st.form_submit_button("Save Assessment")

                        if assess_submitted:
                            a_errors = []
                            if not assessed_type.strip():
                                a_errors.append("Incident / attack type classification is required.")
                            if assessed_sev == "Unassigned":
                                a_errors.append("Please determine a formal severity level.")
                            if a_errors:
                                for e in a_errors:
                                    st.error(e)
                            else:
                                ok, msg = q.assess_incident(
                                    incident_id=incident_id,
                                    incident_type=assessed_type.strip(),
                                    severity=assessed_sev,
                                    new_status=assessed_status,
                                    investigator_id=inv_map[assessed_inv],
                                    assessment_notes=assessment_notes,
                                )
                                if ok:
                                    st.success(msg)
                                    st.rerun()
                                else:
                                    st.error(f"Assessment failed: {msg}")

                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("**Direct Lifecycle Status Transition**")
                uc1, uc2 = st.columns([2, 1])
                with uc1:
                    all_statuses = ["Pending Assessment", "Open", "Under Investigation", "Resolved", "Closed"]
                    cur_st = str(d["status"])
                    new_status = st.selectbox(
                        "Transition Status",
                        all_statuses,
                        index=all_statuses.index(cur_st) if cur_st in all_statuses else 0,
                        key=f"upd_stat_{incident_id}",
                    )
                with uc2:
                    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
                    if st.button("Apply Status Transition", key=f"upd_btn_{incident_id}"):
                        ok, msg = q.update_incident_status(incident_id, new_status)
                        if ok:
                            st.success(f"Status transition to '{new_status}' committed.")
                            st.rerun()
                        else:
                            st.error(f"Status update failed: {msg}")

    # ── Tab 3: Report New Incident (Reporter-Facing) ──
    with tab3:
        render_incident_reporting_form(form_key_suffix="tab")


# ══════════════════════════════════════════════════════════════
#  PAGE 3 – Security Alerts
# ══════════════════════════════════════════════════════════════

def page_alerts():
    st.markdown("<div class='page-title'>Security Alerts</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Telemetry anomalies, firewall notifications, and IP correlation records</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["All Alerts", "Alert Activity Logs"])

    with tab1:
        fc1, fc2 = st.columns(2)
        with fc1:
            sev_f = st.selectbox("Filter by Alert Severity", ["All", "Critical", "High", "Medium", "Low"], key="al_sev")
        with fc2:
            df_tmp = q.get_all_alerts()
            types_a = ["All"] + (sorted(df_tmp["alert_type"].dropna().unique().tolist()) if not df_tmp.empty and "alert_type" in df_tmp.columns else [])
            type_f = st.selectbox("Filter by Alert Classification", types_a, key="al_type")

        df_alerts = q.get_all_alerts(severity=sev_f, alert_type=type_f)

        if not df_alerts.empty:
            critical_count = len(df_alerts[df_alerts["severity"] == "Critical"])
            high_count = len(df_alerts[df_alerts["severity"] == "High"])
            if critical_count:
                st.markdown(f"""
                <div style="background:#2B1D20;border:1px solid #5C2B32;border-left:3px solid #E06C75;border-radius:6px;padding:12px 16px;margin-bottom:12px;color:#E06C75;font-weight:500;">
                    <b>Action Required:</b> {critical_count} Critical severity alert(s) detected requiring containment.
                </div>
                """, unsafe_allow_html=True)
            if high_count:
                st.markdown(f"""
                <div style="background:#2A241C;border:1px solid #5C4325;border-left:3px solid #E58E3C;border-radius:6px;padding:12px 16px;margin-bottom:12px;color:#E58E3C;font-weight:500;">
                    <b>Elevated Risk:</b> {high_count} High-severity alert(s) under observation.
                </div>
                """, unsafe_allow_html=True)

            search_a = st.text_input("Search alert logs...", key="alert_search")
            if search_a:
                mask = df_alerts.apply(lambda r: r.astype(str).str.contains(search_a, case=False).any(), axis=1)
                df_alerts = df_alerts[mask]

            st.markdown(f"**{len(df_alerts)} security alert(s) documented**")
            st.dataframe(df_alerts, use_container_width=True, hide_index=True)

            st.download_button(
                "Export Alerts CSV",
                data=df_to_csv(df_alerts),
                file_name="alerts.csv",
                mime="text/csv",
            )
        else:
            st.info("No security alerts found.")

    with tab2:
        section_header("Automated Alert Activity Logs")
        df_logs = q.get_alert_logs()
        if not df_logs.empty:
            st.dataframe(df_logs, use_container_width=True, hide_index=True)
            st.download_button(
                "Export Alert Logs CSV",
                data=df_to_csv(df_logs),
                file_name="alert_logs.csv",
                mime="text/csv",
            )
        else:
            st.info("No alert logs recorded.")


# ══════════════════════════════════════════════════════════════
#  PAGE 4 – Evidence Tracking
# ══════════════════════════════════════════════════════════════

def page_evidence():
    st.markdown("<div class='page-title'>Evidence Tracking</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Chain of custody, forensic artifacts, memory dumps, and captured packet traces</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Evidence Records", "Register Evidence"])

    with tab1:
        df_inc_all = q.get_all_incidents()
        inc_options = {"All Incidents": None}
        if not df_inc_all.empty:
            for _, r in df_inc_all.iterrows():
                inc_options[f"#{r['incident_id']} - {r['incident_type']}"] = r["incident_id"]

        sel_inc = st.selectbox("Filter Artifacts by Linked Incident", list(inc_options.keys()), key="ev_inc_filter")
        inc_id_filter = inc_options[sel_inc]

        df_ev = q.get_all_evidence(incident_id=inc_id_filter)
        if not df_ev.empty:
            search_e = st.text_input("Search evidence records...", key="ev_search")
            if search_e:
                mask = df_ev.apply(lambda r: r.astype(str).str.contains(search_e, case=False).any(), axis=1)
                df_ev = df_ev[mask]

            st.markdown(f"**{len(df_ev)} forensic evidence record(s)**")
            st.dataframe(df_ev, use_container_width=True, hide_index=True)

            section_header("Forensic Artifact Detail Cards")
            for _, row in df_ev.iterrows():
                sev_c = SEV_COLORS.get(str(row.get("severity", "")), "#777A82")
                with st.expander(f"Artifact #{row['evidence_id']} — {row['evidence_type']} (Incident #{row['incident_id']})"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**Artifact Category:** {row['evidence_type']}")
                        st.markdown(f"**Associated Incident:** #{row['incident_id']} &mdash; {row.get('incident_type', '')}")
                        st.markdown(f"**Incident Severity:** <span style='color:{sev_c};font-weight:600;'>{row.get('severity','')}</span>", unsafe_allow_html=True)
                        st.markdown(f"**Originating User:** {row.get('affected_user','')}")
                    with c2:
                        st.markdown(f"**Collection Timestamp:** {row['collected_at']}")
                        st.markdown(f"**File Reference:** `{row.get('file_reference','N/A')}`")
                    st.markdown(f"**Forensic Description:** {row['description']}")

            st.download_button(
                "Export Evidence CSV",
                data=df_to_csv(df_ev),
                file_name="evidence.csv",
                mime="text/csv",
            )
        else:
            st.info("No evidence records cataloged.")

    with tab2:
        section_header("Register Forensic Evidence Artifact")
        with st.form("add_evidence_form"):
            df_inc_opt = q.get_all_incidents()
            if df_inc_opt.empty:
                st.warning("No incidents available to link evidence to.")
                st.form_submit_button("Record Evidence", disabled=True)
            else:
                ev_inc_map = {f"#{r['incident_id']} - {r['incident_type']} [{r['severity']}]": r["incident_id"] for _, r in df_inc_opt.iterrows()}
                ec1, ec2 = st.columns(2)
                with ec1:
                    ev_inc = st.selectbox("Associated Incident *", list(ev_inc_map.keys()), key="ev_inc_sel")
                    ev_type = st.text_input("Evidence Type *", placeholder="e.g. Memory Dump, Email Header, Syslog Extract")
                with ec2:
                    ev_file = st.text_input("Storage / File Reference", placeholder="e.g. /evidence/incident_12/memdump.raw")
                ev_desc = st.text_area("Forensic Analysis & Preservation Notes *", placeholder="Document chain of custody, hash values, or collection details...", height=100)
                ev_submitted = st.form_submit_button("Register Evidence")
                if ev_submitted:
                    if not ev_type.strip():
                        st.error("Evidence classification is required.")
                    elif not ev_desc.strip():
                        st.error("Preservation description is required.")
                    else:
                        ok, msg = q.add_evidence(
                            incident_id=ev_inc_map[ev_inc],
                            evidence_type=ev_type.strip(),
                            description=ev_desc.strip(),
                            file_reference=ev_file.strip() if ev_file.strip() else None,
                        )
                        if ok:
                            st.success("Evidence record registered successfully.")
                            st.rerun()
                        else:
                            st.error(f"Evidence registration failed: {msg}")


# ══════════════════════════════════════════════════════════════
#  PAGE 5 – Investigation Activities
# ══════════════════════════════════════════════════════════════

def page_investigation_activities():
    st.markdown("<div class='page-title'>Investigation Activities</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Chronological investigator action audit log, containment notes, and remediation tracking</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Activity Audit Log", "Record Investigation Action"])

    with tab1:
        fc1, fc2 = st.columns(2)
        with fc1:
            df_inc_all = q.get_all_incidents()
            inc_opts = {"All Incidents": None}
            if not df_inc_all.empty:
                for _, r in df_inc_all.iterrows():
                    inc_opts[f"#{r['incident_id']} - {r['incident_type']}"] = r["incident_id"]
            sel_inc_act = st.selectbox("Filter by Incident", list(inc_opts.keys()), key="act_inc")
            inc_id_act = inc_opts[sel_inc_act]
        with fc2:
            inv_df = q.get_all_investigators()
            inv_opts = {"All Investigators": None}
            if not inv_df.empty:
                for _, r in inv_df.iterrows():
                    inv_opts[f"{r['name']} ({r['role']})"] = r["investigator_id"]
            sel_inv_act = st.selectbox("Filter by Investigator", list(inv_opts.keys()), key="act_inv")
            inv_id_act = inv_opts[sel_inv_act]

        df_logs = q.get_investigation_logs(incident_id=inc_id_act, investigator_id=inv_id_act)

        if not df_logs.empty:
            search_act = st.text_input("Search action records...", key="act_search")
            if search_act:
                mask = df_logs.apply(lambda r: r.astype(str).str.contains(search_act, case=False).any(), axis=1)
                df_logs = df_logs[mask]

            st.markdown(f"**{len(df_logs)} recorded investigation action(s)**")

            section_header("Chronological Investigation Timeline")
            df_sorted = df_logs.sort_values("action_timestamp", ascending=True)
            for _, row in df_sorted.iterrows():
                sev_c = SEV_COLORS.get(str(row.get("severity", "")), "#777A82")
                st.markdown(
                    f"""
                    <div style="background:#24262B;border:1px solid #35373D;border-left:3px solid #E99B83;border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:12px;">
                        <div style="font-size:0.75rem;color:#777A82;margin-bottom:4px;">
                            {row['action_timestamp']} &nbsp;&bull;&nbsp; <span style="color:#E99B83;font-weight:600;">{row['investigator_name']}</span> <span style="color:#A5A5AA;">({row['investigator_role']})</span>
                        </div>
                        <div style="font-size:0.94rem;color:#F4F1EF;margin-bottom:6px;">
                            <b>Incident #{row['incident_id']}</b> &mdash; {row['incident_type']} <span style="color:{sev_c};font-weight:600;">[{row['severity']}]</span>
                        </div>
                        <div style="font-size:0.88rem;color:#A5A5AA;line-height:1.5;">{row['action_performed']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("<hr>", unsafe_allow_html=True)
            st.dataframe(df_logs, use_container_width=True, hide_index=True)
            st.download_button(
                "Export Activity Log CSV",
                data=df_to_csv(df_logs),
                file_name="investigation_activities.csv",
                mime="text/csv",
            )
        else:
            st.info("No investigation activities logged.")

    with tab2:
        section_header("Log Investigation Action")
        with st.form("log_activity_form"):
            df_inc_opt2 = q.get_all_incidents()
            inv_df2 = q.get_all_investigators()

            if df_inc_opt2.empty:
                st.warning("No incidents available.")
                st.form_submit_button("Record Action", disabled=True)
            elif inv_df2.empty:
                st.warning("No investigators available.")
                st.form_submit_button("Record Action", disabled=True)
            else:
                inc_map2 = {f"#{r['incident_id']} - {r['incident_type']} [{r['severity']}]": r["incident_id"] for _, r in df_inc_opt2.iterrows()}
                inv_map3 = {f"{r['name']} ({r['role']})": r["investigator_id"] for _, r in inv_df2.iterrows()}

                lc1, lc2 = st.columns(2)
                with lc1:
                    sel_inc2 = st.selectbox("Target Incident *", list(inc_map2.keys()), key="log_inc")
                with lc2:
                    sel_inv3 = st.selectbox("Acting Investigator *", list(inv_map3.keys()), key="log_inv")

                action = st.text_area("Action Performed *", placeholder="Specify containment steps taken, host isolation, or forensic findings...", height=110)
                log_submitted = st.form_submit_button("Record Activity")
                if log_submitted:
                    if not action.strip():
                        st.error("Action details are required.")
                    else:
                        ok, msg = q.add_investigation_log(
                            incident_id=inc_map2[sel_inc2],
                            investigator_id=inv_map3[sel_inv3],
                            action_performed=action.strip(),
                        )
                        if ok:
                            st.success("Investigation action logged successfully.")
                            st.rerun()
                        else:
                            st.error(f"Failed to log action: {msg}")


# ══════════════════════════════════════════════════════════════
#  PAGE 6 – Data Entry / Record Management
# ══════════════════════════════════════════════════════════════

def page_record_management():
    st.markdown("<div class='page-title'>Data Entry & Record Management</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Centralized registration hub for reporting incidents, submitting digital evidence, and logging SOC analyst activities</div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "Report New Incident",
        "Add Evidence Record",
        "Log Investigation Action",
    ])

    with tab1:
        render_incident_reporting_form(form_key_suffix="mgmt")

    with tab2:
        section_header("Register Forensic Evidence")
        with st.form("mgmt_add_evidence_form"):
            df_inc_opt = q.get_all_incidents()
            if df_inc_opt.empty:
                st.warning("No incidents available to link evidence to.")
                st.form_submit_button("Submit Evidence", disabled=True)
            else:
                ev_inc_map = {f"#{r['incident_id']} - {r['incident_type']} [{r['severity']}]": r["incident_id"] for _, r in df_inc_opt.iterrows()}
                ec1, ec2 = st.columns(2)
                with ec1:
                    ev_inc = st.selectbox("Associated Incident *", list(ev_inc_map.keys()), key="mgmt_ev_inc")
                    ev_type = st.text_input("Evidence Type *", placeholder="e.g. Email Screenshot, Firewall Log")
                with ec2:
                    ev_file = st.text_input("Storage Location / Reference", placeholder="e.g. evidence/network_dump.pcap")
                ev_desc = st.text_area("Preservation Description *", placeholder="Preservation notes, hash verification, or relevant context...", height=100)
                ev_sub = st.form_submit_button("Submit Evidence Record")
                if ev_sub:
                    if not ev_type.strip():
                        st.error("Evidence classification is required.")
                    elif not ev_desc.strip():
                        st.error("Description is required.")
                    else:
                        ok, msg = q.add_evidence(
                            incident_id=ev_inc_map[ev_inc],
                            evidence_type=ev_type.strip(),
                            description=ev_desc.strip(),
                            file_reference=ev_file.strip() if ev_file.strip() else None,
                        )
                        if ok:
                            st.success("Evidence record saved successfully.")
                            st.rerun()
                        else:
                            st.error(f"Submission failed: {msg}")

    with tab3:
        section_header("Log Investigation Action")
        with st.form("mgmt_log_activity_form"):
            df_inc_opt2 = q.get_all_incidents()
            inv_df2 = q.get_all_investigators()

            if df_inc_opt2.empty or inv_df2.empty:
                st.warning("Incidents and investigators must be available.")
                st.form_submit_button("Record Action", disabled=True)
            else:
                inc_map2 = {f"#{r['incident_id']} - {r['incident_type']} [{r['severity']}]": r["incident_id"] for _, r in df_inc_opt2.iterrows()}
                inv_map3 = {f"{r['name']} ({r['role']})": r["investigator_id"] for _, r in inv_df2.iterrows()}

                lc1, lc2 = st.columns(2)
                with lc1:
                    sel_inc2 = st.selectbox("Target Incident *", list(inc_map2.keys()), key="mgmt_log_inc")
                with lc2:
                    sel_inv3 = st.selectbox("Investigator *", list(inv_map3.keys()), key="mgmt_log_inv")

                action = st.text_area("Investigation Action *", placeholder="Describe triage, evidence review, or system isolation steps...", height=110)
                log_sub = st.form_submit_button("Log Action")
                if log_sub:
                    if not action.strip():
                        st.error("Action description is required.")
                    else:
                        ok, msg = q.add_investigation_log(
                            incident_id=inc_map2[sel_inc2],
                            investigator_id=inv_map3[sel_inv3],
                            action_performed=action.strip(),
                        )
                        if ok:
                            st.success("Investigation action logged successfully.")
                            st.rerun()
                        else:
                            st.error(f"Action logging failed: {msg}")


# ══════════════════════════════════════════════════════════════
#  PAGE 7 – Analytical Insights
# ══════════════════════════════════════════════════════════════

def page_insights():
    st.markdown("<div class='page-title'>Analytical Insights</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>SQL-aggregated intelligence, threat actor metrics, and analyst workload distribution</div>", unsafe_allow_html=True)

    # 1. Critical & High-Severity Incidents
    section_header("Critical & High-Severity Incidents Requiring Triage")
    df_crit = q.get_critical_high_incidents()
    if not df_crit.empty:
        st.dataframe(df_crit, use_container_width=True, hide_index=True)
    else:
        st.info("No critical or high-severity incidents active.")

    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # 2. Suspicious IP Addresses
    with col1:
        section_header("Frequent Suspicious IP Addresses")
        df_ips = q.get_suspicious_ips()
        if not df_ips.empty:
            st.dataframe(df_ips, use_container_width=True, hide_index=True)
            ip_chart = df_ips.set_index("ip_address")[["alert_count"]]
            st.bar_chart(ip_chart, color="#E06C75")
        else:
            st.info("No correlated suspicious IP records.")

    # 3. Attack Type Breakdown
    with col2:
        section_header("Recurring Attack Type Distribution")
        df_att = q.get_attack_type_analysis()
        if not df_att.empty:
            st.dataframe(df_att, use_container_width=True, hide_index=True)
            att_chart = df_att.set_index("incident_type")[["total", "critical_count", "high_count"]]
            st.bar_chart(att_chart, color=[THEME_PEACH, "#E06C75", "#E58E3C"])
        else:
            st.info("No attack classification data.")

    st.markdown("<hr>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    # 4. Investigator Workload
    with col3:
        section_header("Investigator Case Workload")
        df_wl = q.get_investigator_workload()
        if not df_wl.empty:
            st.dataframe(df_wl, use_container_width=True, hide_index=True)
            wl_chart = df_wl.set_index("investigator_name")[["total_incidents"]]
            st.bar_chart(wl_chart, color=THEME_PEACH)
        else:
            st.info("No investigator workload statistics.")

    # 5. Investigation Progress by Status
    with col4:
        section_header("Investigation Progress Status")
        df_prog = q.get_investigation_progress()
        if not df_prog.empty:
            st.dataframe(df_prog, use_container_width=True, hide_index=True)
            prog_chart = df_prog.set_index("status")[["incident_count", "total_actions"]]
            st.bar_chart(prog_chart, color=[THEME_PEACH, THEME_AMBER])
        else:
            st.info("No progress data available.")

    st.markdown("<hr>", unsafe_allow_html=True)

    # 6. Alert Trends
    section_header("Alert Velocity Trends Over Time")
    df_at = q.get_alert_trends()
    if not df_at.empty:
        df_at["date"] = pd.to_datetime(df_at["date"])
        pivot = df_at.pivot_table(index="date", columns="severity", values="count", aggfunc="sum", fill_value=0)
        st.line_chart(pivot)
    else:
        st.info("No alert trend telemetry.")

    # 7. Resolution Patterns
    section_header("Incident Resolution Timing Patterns")
    df_res = q.get_resolution_patterns()
    if not df_res.empty:
        st.dataframe(df_res, use_container_width=True, hide_index=True)
    else:
        st.info("No resolved incidents recorded yet. Resolution duration patterns will populate once incidents are resolved.")


# ══════════════════════════════════════════════════════════════
#  PAGE 8 – Reports & Export
# ══════════════════════════════════════════════════════════════

def page_reports():
    st.markdown("<div class='page-title'>Reports & Export</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Exportable compliance reports, executive summaries, and case resolution logs</div>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Incident Summary",
        "Critical Threat Report",
        "Resolution Summary",
        "Investigator Workload",
    ])

    # ── Tab 1: Incident Summary ──
    with tab1:
        section_header("Executive Incident Summary Report")
        st.caption("Aggregated from database view `Incident_Report`")
        df_rep = q.get_incident_summary_report()
        if not df_rep.empty:
            rfc1, rfc2, rfc3 = st.columns(3)
            with rfc1:
                rsev = st.selectbox("Filter Severity", ["All", "Critical", "High", "Medium", "Low", "Unassigned"], key="rep_sev")
            with rfc2:
                rstat = st.selectbox("Filter Lifecycle Status", ["All", "Pending Assessment", "Open", "Under Investigation", "Resolved", "Closed"], key="rep_stat")
            with rfc3:
                rsearch = st.text_input("Filter report rows...", key="rep_search")

            df_filtered = df_rep.copy()
            if rsev != "All":
                df_filtered = df_filtered[df_filtered["severity"] == rsev]
            if rstat != "All":
                df_filtered = df_filtered[df_filtered["status"] == rstat]
            if rsearch:
                mask = df_filtered.apply(lambda r: r.astype(str).str.contains(rsearch, case=False).any(), axis=1)
                df_filtered = df_filtered[mask]

            st.markdown(f"**{len(df_filtered)} documented case(s)**")
            st.dataframe(df_filtered, use_container_width=True, hide_index=True)

            st.download_button(
                "Export Incident Summary CSV",
                data=df_to_csv(df_filtered),
                file_name="incident_summary_report.csv",
                mime="text/csv",
            )
        else:
            st.info("No incident report records.")

    # ── Tab 2: Critical Incident Report ──
    with tab2:
        section_header("High & Critical Threat Exposure Report")
        st.caption("Aggregated from database view `Critical_Incident_Report`")
        df_crit = q.get_critical_high_incidents()
        if not df_crit.empty:
            st.markdown(f"""
            <div style="background:#2B1D20;border:1px solid #5C2B32;border-left:3px solid #E06C75;border-radius:6px;padding:12px 16px;margin-bottom:14px;color:#E06C75;font-weight:500;">
                <b>Action Required:</b> {len(df_crit)} critical/high-severity incident(s) require prioritized investigator attention.
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(df_crit, use_container_width=True, hide_index=True)
            st.download_button(
                "Export Critical Incident CSV",
                data=df_to_csv(df_crit),
                file_name="critical_incident_report.csv",
                mime="text/csv",
            )
        else:
            st.success("No active critical or high-severity security incidents.")

    # ── Tab 3: Resolution Summary ──
    with tab3:
        section_header("Incident Resolution Duration Summary")
        st.caption("Calculated using database function `CalculateResolutionDuration()`")
        df_res = q.get_resolution_summary()
        if not df_res.empty:
            st.dataframe(df_res, use_container_width=True, hide_index=True)
            st.download_button(
                "Export Resolution CSV",
                data=df_to_csv(df_res),
                file_name="resolution_report.csv",
                mime="text/csv",
            )
        else:
            st.info("No resolution telemetry documented.")

    # ── Tab 4: Workload Report ──
    with tab4:
        section_header("Investigator Workload Compliance Report")
        st.caption("Aggregated from database view `Investigator_Workload_Report`")
        df_wl = q.get_investigator_workload()
        if not df_wl.empty:
            st.dataframe(df_wl, use_container_width=True, hide_index=True)
            wl_bar = df_wl.set_index("investigator_name")[["total_incidents"]]
            st.bar_chart(wl_bar, color=THEME_PEACH)
            st.download_button(
                "Export Workload CSV",
                data=df_to_csv(df_wl),
                file_name="investigator_workload_report.csv",
                mime="text/csv",
            )
        else:
            st.info("No workload metrics documented.")


# ══════════════════════════════════════════════════════════════
#  Application Router
# ══════════════════════════════════════════════════════════════

if page == "Dashboard Overview":
    page_overview()
elif page == "Incident Investigation":
    page_incidents()
elif page == "Security Alerts":
    page_alerts()
elif page == "Evidence Tracking":
    page_evidence()
elif page == "Investigation Activities":
    page_investigation_activities()
elif page == "Data Entry / Record Management":
    page_record_management()
elif page == "Analytical Insights":
    page_insights()
elif page in ("Reports", "Reports & Export"):
    page_reports()
