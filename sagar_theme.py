"""
╔══════════════════════════════════════════════════════════╗
║  sagar_theme.py — Sagar AI Design System  v2.1           ║
║  Compact single-screen light theme. No scroll on load.   ║
╚══════════════════════════════════════════════════════════╝
"""

import streamlit as st

THEME = {
    "bg":           "#F5F3EE",
    "bg2":          "#FFFFFF",
    "bg_header":    "#0C1E2C",
    "primary":      "#C9A84C",
    "primary_lt":   "#E8C97A",
    "primary_dim":  "rgba(201,168,76,0.08)",
    "domain":       "#1D6FA4",
    "domain_dim":   "rgba(29,111,164,0.07)",
    "text":         "#0C1E2C",
    "text2":        "#3A5068",
    "muted":        "#8A9BAA",
    "border":       "#E6E0D8",
    "border2":      "rgba(201,168,76,0.28)",
    "success":      "#1A9E7A",
    "warning":      "#C85A1A",
    "error":        "#D94040",
    "shadow":       "0 1px 4px rgba(12,30,44,0.07), 0 4px 12px rgba(12,30,44,0.05)",
    "shadow_md":    "0 4px 20px rgba(12,30,44,0.11)",
    "font_display": "'Cormorant Garamond', serif",
    "font_heading": "'Outfit', sans-serif",
    "font_body":    "'DM Sans', sans-serif",
    "font_mono":    "'JetBrains Mono', monospace",
}


def apply_theme():
    t = THEME
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300&family=Outfit:wght@400;500;600;700&family=DM+Sans:wght@400;500&family=JetBrains+Mono:wght@400&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after {{ box-sizing: border-box; }}
html, body, [class*="css"] {{
    font-family: {t['font_body']};
    -webkit-font-smoothing: antialiased;
}}
.stApp {{ background: {t['bg']} !important; color: {t['text']}; }}
#MainMenu, footer, header {{ visibility: hidden; }}

/* ── Tight container — no wasted vertical space ── */
.block-container {{
    padding-top: 0 !important;
    padding-bottom: 0.5rem !important;
    max-width: 1200px !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
}}

/* ── Column gap tightening ── */
[data-testid="column"] {{ padding: 0 8px !important; }}

/* ── Labels — soft, sentence-case, never screaming ── */
.stTextArea label,
.stSelectbox label,
.stRadio label {{
    color: {t['text2']} !important;
    font-family: {t['font_heading']} !important;
    font-size: 0.76rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.01em !important;
    text-transform: none !important;
    margin-bottom: 3px !important;
}}

/* ── Textarea ── */
.stTextArea textarea {{
    background: {t['bg2']} !important;
    border: 1.5px solid {t['border']} !important;
    border-radius: 10px !important;
    color: {t['text']} !important;
    font-family: {t['font_body']} !important;
    font-size: 0.875rem !important;
    line-height: 1.65 !important;
    padding: 10px 13px !important;
    resize: none !important;
    box-shadow: inset 0 1px 2px rgba(12,30,44,0.04) !important;
    transition: border-color 0.18s, box-shadow 0.18s !important;
}}
.stTextArea textarea:focus {{
    border-color: {t['domain']} !important;
    box-shadow: 0 0 0 3px {t['domain_dim']}, inset 0 1px 2px rgba(12,30,44,0.04) !important;
    outline: none !important;
}}
.stTextArea textarea::placeholder {{
    color: {t['muted']} !important;
    opacity: 0.65 !important;
    font-style: italic !important;
}}

/* ── Selectbox ── */
.stSelectbox > div > div {{
    background: {t['bg2']} !important;
    border: 1.5px solid {t['border']} !important;
    border-radius: 8px !important;
    color: {t['text']} !important;
    font-family: {t['font_body']} !important;
    font-size: 0.875rem !important;
    box-shadow: {t['shadow']} !important;
    min-height: 38px !important;
}}
.stSelectbox > div > div:focus-within {{
    border-color: {t['domain']} !important;
    box-shadow: 0 0 0 3px {t['domain_dim']} !important;
}}
/* Dropdown list */
[data-baseweb="popover"] ul {{
    background: {t['bg2']} !important;
    border: 1.5px solid {t['border']} !important;
    border-radius: 8px !important;
    box-shadow: {t['shadow_md']} !important;
}}
[data-baseweb="popover"] li {{
    font-family: {t['font_body']} !important;
    font-size: 0.875rem !important;
    color: {t['text']} !important;
}}
[data-baseweb="popover"] li:hover {{
    background: {t['domain_dim']} !important;
}}

/* ── Primary button ── */
.stButton > button {{
    background: {t['text']} !important;
    color: #F5F3EE !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: {t['font_heading']} !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.04em !important;
    width: 100% !important;
    padding: 0.68rem 1.5rem !important;
    transition: background 0.18s, transform 0.15s, box-shadow 0.18s !important;
    box-shadow: {t['shadow_md']} !important;
    cursor: pointer !important;
}}
.stButton > button:hover {{
    background: {t['primary']} !important;
    color: {t['text']} !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(201,168,76,0.32) !important;
}}
.stButton > button:active {{ transform: translateY(0) !important; }}
.stButton > button:disabled {{
    background: {t['border']} !important;
    color: {t['muted']} !important;
    box-shadow: none !important;
    transform: none !important;
    cursor: not-allowed !important;
}}

/* ── Download button ── */
.stDownloadButton > button {{
    background: {t['bg2']} !important;
    color: {t['domain']} !important;
    border: 1.5px solid rgba(29,111,164,0.22) !important;
    border-radius: 8px !important;
    font-family: {t['font_heading']} !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    width: 100% !important;
    transition: all 0.18s !important;
    box-shadow: {t['shadow']} !important;
}}
.stDownloadButton > button:hover {{
    background: {t['domain_dim']} !important;
    border-color: {t['domain']} !important;
    transform: translateY(-1px) !important;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1.5px solid {t['border']} !important;
    gap: 0 !important;
    padding-bottom: 0 !important;
}}
.stTabs [data-baseweb="tab"] {{
    font-family: {t['font_heading']} !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    color: {t['muted']} !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 0.6rem 1rem !important;
    margin-bottom: -1.5px !important;
    transition: color 0.15s !important;
}}
.stTabs [data-baseweb="tab"]:hover {{ color: {t['text2']} !important; }}
.stTabs [aria-selected="true"] {{
    color: {t['domain']} !important;
    border-bottom-color: {t['domain']} !important;
    font-weight: 600 !important;
}}

/* ── Metrics ── */
[data-testid="metric-container"] {{
    background: {t['bg2']} !important;
    border: 1.5px solid {t['border']} !important;
    border-radius: 10px !important;
    padding: 0.75rem 1rem !important;
    box-shadow: {t['shadow']} !important;
    transition: all 0.18s !important;
}}
[data-testid="metric-container"]:hover {{
    border-color: {t['primary']} !important;
    box-shadow: 0 3px 14px rgba(201,168,76,0.14) !important;
    transform: translateY(-1px) !important;
}}
[data-testid="metric-container"] label {{
    color: {t['muted']} !important;
    font-size: 0.65rem !important;
    font-family: {t['font_heading']} !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}}
[data-testid="stMetricValue"] {{
    color: {t['text']} !important;
    font-family: {t['font_display']} !important;
    font-size: 2rem !important;
    font-weight: 400 !important;
    line-height: 1.1 !important;
}}

/* ── Alerts ── */
.stAlert {{
    background: {t['bg2']} !important;
    border: 1.5px solid {t['border']} !important;
    border-radius: 10px !important;
    box-shadow: {t['shadow']} !important;
    font-size: 0.86rem !important;
}}

/* ── Expander ── */
.streamlit-expanderHeader {{
    font-family: {t['font_heading']} !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: {t['text2']} !important;
    background: {t['bg2']} !important;
    border: 1.5px solid {t['border']} !important;
    border-radius: 8px !important;
    padding: 0.5rem 0.9rem !important;
}}
.streamlit-expanderContent {{
    background: {t['bg2']} !important;
    border: 1.5px solid {t['border']} !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    padding: 0.75rem !important;
}}

/* ── Spinner ── */
.stSpinner > div {{ border-top-color: {t['primary']} !important; }}

/* ── Divider ── */
hr {{ border-color: {t['border']} !important; margin: 0.75rem 0 !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 4px; height: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: rgba(201,168,76,0.28); border-radius: 4px; }}
::-webkit-scrollbar-thumb:hover {{ background: {t['primary']}; }}
</style>
""", unsafe_allow_html=True)


# ────────────────────────────────────────────────────────
# UI COMPONENTS
# ────────────────────────────────────────────────────────

def header(app_name: str, app_suffix: str = "AI", tagline: str = "AI Test Case Generator"):
    t = THEME
    # Use ⬡ emoji reliably instead of SVG (avoids Streamlit stripping inline SVG)
    st.markdown(f"""
<div style="
    background:{t['bg_header']};
    padding:12px 28px;
    margin: 0 -1.25rem 1.25rem -1.25rem;
    display:flex; align-items:center; justify-content:space-between;
    gap:16px;
">
  <div style="display:flex;align-items:center;gap:11px;flex-shrink:0;">
    <div style="
        width:32px; height:32px; border-radius:8px;
        background:{t['primary']};
        display:flex; align-items:center; justify-content:center;
        font-size:16px; line-height:1; color:{t['text']};
        font-family:{t['font_heading']}; font-weight:700;
    ">⬡</div>
    <span style="
        font-family:{t['font_display']}; font-size:1.55rem; font-weight:400;
        letter-spacing:0.07em; color:#F5F3EE; line-height:1;
    ">{app_name}<em style="color:{t['primary_lt']};font-style:italic;">{app_suffix}</em></span>
  </div>
  <span style="
      font-family:{t['font_mono']}; font-size:0.58rem; letter-spacing:0.22em;
      color:rgba(201,168,76,0.5); text-transform:uppercase;
  ">{tagline}</span>
  <span style="
      font-family:{t['font_mono']}; font-size:0.55rem; letter-spacing:0.1em;
      color:rgba(255,255,255,0.16);
  ">v2.1</span>
</div>
<div style="
    height:2px; margin:-1.25rem -1.25rem 1.25rem -1.25rem;
    background:linear-gradient(90deg,{t['primary']} 0%,rgba(201,168,76,0.08) 50%,transparent 100%);
"></div>
""", unsafe_allow_html=True)


def section_label(text: str, top_margin: str = "0"):
    """Minimal section divider label — replaces card_title."""
    t = THEME
    st.markdown(f"""
<div style="
    display:flex; align-items:center; gap:8px;
    margin: {top_margin} 0 8px 0;
">
  <div style="width:3px; height:14px; background:{t['primary']}; border-radius:2px; flex-shrink:0;"></div>
  <span style="
      font-family:{t['font_heading']}; font-size:0.68rem; font-weight:700;
      letter-spacing:0.16em; text-transform:uppercase; color:{t['text2']};
  ">{text}</span>
</div>
""", unsafe_allow_html=True)


# Keep card_title as alias for backward compat
def card_title(text: str, margin_top: bool = False, domain_color: bool = False):
    top = "12px" if margin_top else "0"
    section_label(text, top_margin=top)


def metric_row(metrics: list):
    cols = st.columns(len(metrics))
    for col, m in zip(cols, metrics):
        col.metric(m["label"], m["value"])


def result_block(tc: dict):
    t = THEME
    p_meta = {
        "High":   ("#D94040", "rgba(217,64,64,0.07)"),
        "Medium": ("#C85A1A", "rgba(200,90,26,0.07)"),
        "Low":    ("#1A9E7A", "rgba(26,158,122,0.07)"),
    }
    p_color, p_bg = p_meta.get(tc.get("priority",""), (t['muted'], t['primary_dim']))

    cat_color_map = {
        "Functional":  t['domain'],
        "Edge Case":   "#5B4FCF",
        "Negative":    t['warning'],
        "Security":    t['error'],
        "Performance": t['success'],
        "UI/UX":       "#1A6B8A",
    }
    cat_color = cat_color_map.get(tc.get("category",""), t['muted'])

    steps_html = "".join(
        f'<div style="display:flex;gap:9px;margin:4px 0;align-items:flex-start;">'
        f'<span style="font-family:{t["font_mono"]};font-size:0.6rem;color:{t["domain"]};'
        f'min-width:18px;padding-top:3px;opacity:0.8;">{i+1:02d}</span>'
        f'<span style="font-size:0.83rem;color:{t["text2"]};line-height:1.5;">{s}</span></div>'
        for i, s in enumerate(tc.get("steps",[]))
    )
    notes_html = (
        f'<div style="margin-top:8px;padding:7px 11px;background:rgba(138,155,170,0.07);'
        f'border-radius:7px;font-size:0.8rem;color:{t["muted"]};font-style:italic;">'
        f'💬 {tc["notes"]}</div>'
    ) if tc.get("notes") else ""

    st.markdown(f"""
<div style="
    background:{t['bg2']}; border:1.5px solid {t['border']};
    border-left:4px solid {p_color}; border-radius:0 11px 11px 0;
    padding:14px 18px; margin-bottom:9px;
    box-shadow:0 1px 6px rgba(12,30,44,0.05);
">
  <div style="display:flex;align-items:center;justify-content:space-between;
              margin-bottom:9px;flex-wrap:wrap;gap:6px;">
    <div style="display:flex;align-items:center;gap:7px;">
      <span style="font-family:{t['font_mono']};font-size:0.58rem;font-weight:500;
                   color:#fff;background:{t['text']};padding:2px 7px;border-radius:4px;">
        {tc.get('id','TC')}</span>
      <span style="font-size:0.68rem;color:{cat_color};font-family:{t['font_heading']};
                   font-weight:600;background:rgba(29,111,164,0.06);
                   padding:2px 8px;border-radius:4px;">
        {tc.get('category','')}</span>
    </div>
    <span style="font-size:0.7rem;color:{p_color};font-family:{t['font_heading']};
                 font-weight:600;background:{p_bg};padding:2px 9px;border-radius:20px;">
      ● {tc.get('priority','')}</span>
  </div>

  <div style="font-family:{t['font_heading']};font-size:0.93rem;font-weight:600;
              color:{t['text']};line-height:1.3;margin-bottom:11px;">
    {tc.get('title','')}</div>

  <div style="font-size:0.63rem;text-transform:uppercase;letter-spacing:0.11em;
              color:{t['muted']};font-family:{t['font_heading']};font-weight:600;margin-bottom:3px;">
    Preconditions</div>
  <div style="font-size:0.82rem;color:{t['text2']};line-height:1.5;
              padding:5px 9px;background:{t['bg']};border-radius:6px;margin-bottom:8px;">
    {tc.get('preconditions','—')}</div>

  <div style="font-size:0.63rem;text-transform:uppercase;letter-spacing:0.11em;
              color:{t['muted']};font-family:{t['font_heading']};font-weight:600;margin-bottom:3px;">
    Steps</div>
  <div style="padding:4px 7px;background:{t['bg']};border-radius:6px;margin-bottom:8px;">
    {steps_html}</div>

  <div style="font-size:0.63rem;text-transform:uppercase;letter-spacing:0.11em;
              color:{t['muted']};font-family:{t['font_heading']};font-weight:600;margin-bottom:3px;">
    Expected Result</div>
  <div style="font-size:0.82rem;color:{t['success']};font-weight:500;line-height:1.5;
              padding:6px 10px;background:rgba(26,158,122,0.06);
              border-left:3px solid {t['success']};border-radius:0 6px 6px 0;">
    ✓ {tc.get('expected_result','')}</div>
  {notes_html}
</div>
""", unsafe_allow_html=True)


def empty_state(icon: str = "⬡", title: str = "Results will appear here",
                hint: str = "Paste input → Select type → Generate"):
    t = THEME
    st.markdown(f"""
<div style="
    text-align:center; padding:3rem 2rem;
    background:{t['bg2']}; border:2px dashed {t['border']};
    border-radius:14px;
">
  <div style="
      width:52px;height:52px;border-radius:14px;
      background:{t['primary_dim']};border:2px solid {t['border2']};
      display:flex;align-items:center;justify-content:center;
      margin:0 auto 1rem auto;font-size:22px;
  ">{icon}</div>
  <div style="
      font-family:{t['font_display']};font-size:1.3rem;font-weight:400;
      color:{t['muted']};margin-bottom:6px;letter-spacing:0.02em;
  ">{title}</div>
  <div style="
      font-family:{t['font_mono']};font-size:0.58rem;letter-spacing:0.2em;
      color:rgba(138,155,170,0.45);text-transform:uppercase;
  ">{hint}</div>
</div>
""", unsafe_allow_html=True)


def status_indicator(key_name: str, key_set: bool, key_url: str):
    t = THEME
    if key_set:
        color, bg, bdr = t['success'], "rgba(26,158,122,0.07)", "rgba(26,158,122,0.22)"
        icon, text = "✓", f"{key_name} is set"
    else:
        color, bg, bdr = t['warning'], "rgba(200,90,26,0.07)", "rgba(200,90,26,0.22)"
        icon, text = "○", f"Add {key_name} to secrets.toml"
    st.markdown(
        f'<div style="font-family:{t["font_mono"]};font-size:0.63rem;letter-spacing:0.05em;'
        f'color:{color};background:{bg};border:1px solid {bdr};'
        f'border-radius:7px;padding:5px 10px;margin-bottom:4px;">'
        f'{icon} {text} · <a href="https://{key_url}" target="_blank" '
        f'style="color:{color};opacity:0.7;">{key_url}</a></div>',
        unsafe_allow_html=True
    )


def provider_note(text: str):
    t = THEME
    st.markdown(
        f'<div style="font-family:{t["font_mono"]};font-size:0.6rem;'
        f'color:{t["muted"]};margin-top:2px;margin-bottom:6px;line-height:1.5;">'
        f'{text}</div>',
        unsafe_allow_html=True
    )


def highlight_box(title: str, body: str):
    t = THEME
    st.markdown(f"""
<div style="
    background:{t['primary_dim']}; border:1.5px solid {t['border2']};
    border-left:4px solid {t['primary']}; border-radius:0 9px 9px 0;
    padding:10px 14px; margin:6px 0;
">
  <div style="font-family:{t['font_heading']};font-size:0.78rem;font-weight:600;
              color:{t['text']};margin-bottom:4px;">{title}</div>
  <div style="font-size:0.83rem;color:{t['text2']};line-height:1.6;">{body}</div>
</div>
""", unsafe_allow_html=True)


def gap_item(text: str):
    t = THEME
    st.markdown(
        f'<div style="font-size:0.82rem;color:{t["warning"]};padding:4px 10px;'
        f'border-left:3px solid {t["warning"]};margin:3px 0;'
        f'background:rgba(200,90,26,0.05);border-radius:0 6px 6px 0;">⚠ {text}</div>',
        unsafe_allow_html=True
    )


def footer():
    t = THEME
    st.markdown(f"""
<div style="
    margin-top:1.25rem; padding:10px 0 2px;
    border-top:1px solid {t['border']};
    display:flex; justify-content:center; gap:24px; flex-wrap:wrap;
">
  <span style="font-family:{t['font_mono']};font-size:0.56rem;letter-spacing:0.12em;
               text-transform:uppercase;color:{t['muted']};">
    Sagar<em style="font-style:italic;color:{t['primary']};">AI</em>
  </span>
  <span style="font-family:{t['font_mono']};font-size:0.56rem;letter-spacing:0.08em;
               color:rgba(138,155,170,0.4);">
    AI That Runs Deep · C.S. Sagar · © 2025
  </span>
</div>
""", unsafe_allow_html=True)
