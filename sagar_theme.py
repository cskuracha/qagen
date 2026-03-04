"""
╔══════════════════════════════════════════════════════════╗
║  sagar_theme.py — Sagar AI Design System  v1.0           ║
║  Drop this into ANY Sagar AI Streamlit app.               ║
║                                                           ║
║  Usage:                                                   ║
║    from sagar_theme import (                              ║
║        apply_theme, header, card_title, result_block,    ║
║        empty_state, status_indicator, highlight_box,     ║
║        metric_row, footer                                 ║
║    )                                                      ║
║                                                           ║
║  To retheme: edit the THEME dict below. Everything        ║
║  adapts automatically — buttons, tabs, cards, metrics.   ║
╚══════════════════════════════════════════════════════════╝
"""

import streamlit as st

# ── THEME CONFIG ─────────────────────────────────────────
# Edit ONLY this section to retheme all Sagar AI apps
THEME = {
    "bg":           "#020b18",               # page background
    "bg2":          "#0a2540",               # card / panel background
    "primary":      "#0d9488",               # primary color (teal)
    "primary_lt":   "#14b8a6",               # lighter primary
    "primary_dim":  "rgba(13,148,136,0.10)", # tinted bg for cards
    "text":         "#f0f8ff",               # primary text
    "text2":        "#cbd5e1",               # secondary text
    "muted":        "#7baab8",               # muted / placeholder
    "border":       "rgba(255,255,255,0.07)",# default border
    "border2":      "rgba(20,184,166,0.25)", # accent border
    "success":      "#34d399",
    "warning":      "#fbbf24",
    "error":        "#f87171",
    "font_display": "'Cormorant Garamond', Georgia, serif",
    "font_body":    "'Outfit', system-ui, sans-serif",
    "font_mono":    "'DM Mono', monospace",
}


def apply_theme():
    """
    Inject full Sagar AI CSS. Call ONCE at top of app.py,
    right after st.set_page_config().
    """
    t = THEME
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&family=DM+Mono:wght@300;400;500&family=Outfit:wght@200;300;400;500;600&display=swap');

html, body, [class*="css"] {{ font-family: {t['font_body']}; }}
.stApp {{ background: {t['bg']}; color: {t['text']}; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px; }}

/* ── Text inputs ── */
.stTextArea textarea {{
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 2px !important;
    color: {t['text']} !important;
    font-family: {t['font_mono']} !important;
    font-size: 0.85rem !important;
    resize: vertical !important;
}}
.stTextArea textarea:focus {{
    border-color: {t['primary']} !important;
    box-shadow: 0 0 0 2px {t['primary_dim']} !important;
}}
.stTextArea textarea::placeholder {{ color: {t['muted']} !important; }}
.stTextArea label, .stSelectbox label, .stRadio label {{
    color: {t['muted']} !important;
    font-family: {t['font_body']} !important;
    font-size: 0.85rem !important;
}}

/* ── Select boxes ── */
.stSelectbox > div > div {{
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 2px !important;
    color: {t['text']} !important;
}}
.stSelectbox > div > div:focus-within {{
    border-color: {t['primary']} !important;
}}

/* ── Primary button ── */
.stButton > button {{
    background: {t['primary']} !important;
    color: {t['bg']} !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: {t['font_body']} !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    width: 100% !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.2s !important;
}}
.stButton > button:hover {{
    background: {t['primary_lt']} !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 0 20px rgba(13,148,136,0.3) !important;
}}
.stButton > button:active {{ transform: translateY(0) !important; }}

/* ── Download button ── */
.stDownloadButton > button {{
    background: {t['primary_dim']} !important;
    color: {t['primary_lt']} !important;
    border: 1px solid {t['border2']} !important;
    border-radius: 2px !important;
    font-family: {t['font_mono']} !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    width: 100% !important;
    transition: all 0.2s !important;
}}
.stDownloadButton > button:hover {{
    background: rgba(13,148,136,0.2) !important;
    border-color: {t['primary_lt']} !important;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: rgba(255,255,255,0.02) !important;
    border-bottom: 1px solid {t['border']} !important;
    gap: 0 !important;
}}
.stTabs [data-baseweb="tab"] {{
    font-family: {t['font_mono']} !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: {t['muted']} !important;
    background: transparent !important;
    border: none !important;
    padding: 0.75rem 1.2rem !important;
    transition: color 0.2s !important;
}}
.stTabs [aria-selected="true"] {{
    color: {t['primary_lt']} !important;
    border-bottom: 2px solid {t['primary_lt']} !important;
}}

/* ── Metrics ── */
[data-testid="metric-container"] {{
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid {t['border']} !important;
    border-radius: 2px !important;
    padding: 1rem !important;
    transition: all 0.2s !important;
}}
[data-testid="metric-container"]:hover {{
    border-color: {t['border2']} !important;
    background: {t['primary_dim']} !important;
}}
[data-testid="metric-container"] label {{
    color: {t['muted']} !important;
    font-size: 0.72rem !important;
    font-family: {t['font_mono']} !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}}
[data-testid="stMetricValue"] {{
    color: {t['primary_lt']} !important;
    font-family: {t['font_display']} !important;
    font-size: 2rem !important;
    font-weight: 300 !important;
}}

/* ── Alerts ── */
.stAlert {{
    background: {t['primary_dim']} !important;
    border: 1px solid {t['border2']} !important;
    color: {t['primary_lt']} !important;
    border-radius: 2px !important;
}}

/* ── Expander ── */
.streamlit-expanderHeader {{
    font-family: {t['font_mono']} !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    color: {t['muted']} !important;
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid {t['border']} !important;
    border-radius: 2px !important;
}}
.streamlit-expanderContent {{
    background: rgba(255,255,255,0.01) !important;
    border: 1px solid {t['border']} !important;
    border-top: none !important;
}}

/* ── Spinner ── */
.stSpinner > div {{ border-top-color: {t['primary_lt']} !important; }}

/* ── Divider ── */
hr {{ border-color: {t['border']} !important; margin: 1.5rem 0 !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: {t['bg']}; }}
::-webkit-scrollbar-thumb {{ background: rgba(13,148,136,0.35); border-radius: 2px; }}
::-webkit-scrollbar-thumb:hover {{ background: {t['primary']}; }}
</style>
""", unsafe_allow_html=True)


# ── UI Component Library ─────────────────────────────────

def header(app_name: str, app_suffix: str = "AI", tagline: str = "∿ AI That Runs Deep"):
    """Top header with Sagar AI logo and tagline."""
    t = THEME
    st.markdown(f"""
<div style="text-align:center;padding:2.5rem 0 1.5rem;
            border-bottom:1px solid {t['border']};margin-bottom:2rem;">
  <div style="font-family:{t['font_display']};font-size:2.6rem;font-weight:300;
              letter-spacing:0.1em;color:{t['text']};">
    {app_name}<em style="color:{t['primary_lt']};font-style:italic;">{app_suffix}</em>
  </div>
  <div style="font-family:{t['font_mono']};font-size:0.65rem;letter-spacing:0.3em;
              color:{t['primary']};text-transform:uppercase;margin-top:4px;">
    {tagline}
  </div>
</div>
""", unsafe_allow_html=True)


def card_title(text: str, margin_top: bool = False):
    """Teal monospace section label."""
    t = THEME
    mt = "margin-top:1.2rem;" if margin_top else ""
    st.markdown(f"""
<div style="font-family:{t['font_mono']};font-size:0.63rem;letter-spacing:0.22em;
            text-transform:uppercase;color:{t['primary']};margin-bottom:0.8rem;{mt}">
  {text}
</div>
""", unsafe_allow_html=True)


def metric_row(metrics: list):
    """
    Render evenly-spaced metric boxes.
    metrics = [{"value": "42", "label": "Test Cases"}, ...]
    """
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        col.metric(m["label"], m["value"])


def result_block(tc: dict):
    """
    Render a single result card.
    tc = {"id","title","category","priority","preconditions","steps","expected_result","notes","status"}
    """
    t = THEME
    p_colors = {"High": t['error'], "Medium": t['warning'], "Low": t['success']}
    p_color   = p_colors.get(tc.get("priority",""), t['muted'])
    steps_html = "".join(
        f'<div style="margin:3px 0;color:#94a3b8;font-size:0.84rem;">  {i+1}. {s}</div>'
        for i, s in enumerate(tc.get("steps", []))
    )
    notes_html = (
        f'<div style="font-family:{t["font_mono"]};font-size:0.58rem;letter-spacing:0.15em;'
        f'text-transform:uppercase;color:{t["muted"]};margin-top:8px;margin-bottom:3px;">Notes</div>'
        f'<div style="font-size:0.86rem;color:{t["muted"]};font-style:italic;line-height:1.5;">{tc["notes"]}</div>'
    ) if tc.get("notes") else ""

    st.markdown(f"""
<div style="background:rgba(13,148,136,0.04);border:1px solid rgba(20,184,166,0.14);
            border-left:3px solid {t['primary']};border-radius:0 2px 2px 0;
            padding:1.2rem 1.4rem;margin-bottom:0.9rem;">
  <div style="font-family:{t['font_mono']};font-size:0.6rem;letter-spacing:0.2em;
              color:{t['primary']};text-transform:uppercase;margin-bottom:4px;">
    {tc.get('id','TC')} · {tc.get('category','')}
  </div>
  <div style="font-size:1rem;font-weight:600;color:{t['text']};margin-bottom:8px;line-height:1.3;">
    {tc.get('title','')}
  </div>
  <div style="margin-bottom:10px;">
    <span style="color:{p_color};font-weight:600;font-size:0.88rem;">● {tc.get('priority','')}</span>
    <span style="color:{t['muted']};font-size:0.76rem;margin-left:12px;">{tc.get('status','Not Executed')}</span>
  </div>
  <div style="font-family:{t['font_mono']};font-size:0.58rem;letter-spacing:0.15em;
              text-transform:uppercase;color:{t['muted']};margin-bottom:3px;">Preconditions</div>
  <div style="font-size:0.86rem;color:{t['text2']};line-height:1.55;margin-bottom:6px;">{tc.get('preconditions','—')}</div>
  <div style="font-family:{t['font_mono']};font-size:0.58rem;letter-spacing:0.15em;
              text-transform:uppercase;color:{t['muted']};margin-bottom:3px;">Steps</div>
  {steps_html}
  <div style="font-family:{t['font_mono']};font-size:0.58rem;letter-spacing:0.15em;
              text-transform:uppercase;color:{t['muted']};margin-top:8px;margin-bottom:3px;">Expected Result</div>
  <div style="font-size:0.86rem;color:#86efac;line-height:1.55;">{tc.get('expected_result','')}</div>
  {notes_html}
</div>
""", unsafe_allow_html=True)


def empty_state(icon: str = "⬡", title: str = "Results will appear here",
                hint: str = "Paste input → Select type → Generate"):
    """Placeholder shown before any results exist."""
    t = THEME
    st.markdown(f"""
<div style="text-align:center;padding:4rem 2rem;
            border:1px dashed rgba(255,255,255,0.07);border-radius:2px;margin-top:0.5rem;">
  <div style="font-size:2.5rem;margin-bottom:1rem;opacity:0.22;">{icon}</div>
  <div style="font-family:{t['font_display']};font-size:1.3rem;font-weight:300;
              color:{t['muted']};margin-bottom:6px;">{title}</div>
  <div style="font-family:{t['font_mono']};font-size:0.6rem;letter-spacing:0.2em;
              color:rgba(123,170,184,0.3);text-transform:uppercase;">{hint}</div>
</div>
""", unsafe_allow_html=True)


def status_indicator(key_name: str, key_set: bool, key_url: str):
    """Show API key status with a link to get the key."""
    t = THEME
    color = t['success'] if key_set else t['error']
    text  = "API key found ✓" if key_set else f"Add {key_name} to secrets"
    st.markdown(
        f'<div style="font-family:{t["font_mono"]};font-size:0.64rem;letter-spacing:0.1em;'
        f'color:{color};margin-bottom:0.8rem;line-height:1.6;">● {text} · '
        f'<a href="https://{key_url}" target="_blank" style="color:{color};opacity:0.8;">'
        f'{key_url}</a></div>',
        unsafe_allow_html=True
    )


def highlight_box(title: str, body: str):
    """Teal left-border callout / info box."""
    t = THEME
    st.markdown(f"""
<div style="background:{t['primary_dim']};border:1px solid {t['border2']};
            border-left:3px solid {t['primary_lt']};border-radius:0 2px 2px 0;
            padding:1rem 1.2rem;margin:0.8rem 0;">
  <div style="font-size:0.88rem;font-weight:600;color:{t['text']};margin-bottom:5px;">{title}</div>
  <div style="font-size:0.86rem;color:{t['text2']};line-height:1.65;">{body}</div>
</div>
""", unsafe_allow_html=True)


def gap_item(text: str):
    """A warning gap / missing requirement item."""
    t = THEME
    st.markdown(
        f'<div style="font-size:0.84rem;color:{t["warning"]};padding:4px 0;">⚠ {text}</div>',
        unsafe_allow_html=True
    )


def footer():
    """Bottom footer bar."""
    t = THEME
    st.markdown("---")
    st.markdown(f"""
<div style="text-align:center;padding:0.8rem 0 0.2rem;">
  <div style="font-family:{t['font_mono']};font-size:0.6rem;letter-spacing:0.2em;
              color:rgba(123,170,184,0.28);text-transform:uppercase;">
    ∿ Sagar AI · AI That Runs Deep · Built by C.S. Sagar · © 2025
  </div>
</div>
""", unsafe_allow_html=True)
