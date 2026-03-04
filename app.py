"""
╔══════════════════════════════════════════════════════════╗
║  Sagar QA — AI Test Case Generator                       ║
║  Part of Sagar AI · sagar.ai                             ║
║                                                          ║
║  AI Providers:                                           ║
║   ✅ Groq       — FREE, no card needed (default)         ║
║   ✅ Gemini     — FREE, Google account needed            ║
║   🔒 Claude     — Paid, enable in PROVIDER_CONFIG below  ║
║   🔒 OpenAI     — Paid, enable in PROVIDER_CONFIG below  ║
║                                                          ║
║  To enable a paid provider:                              ║
║   1. Add the API key to .streamlit/secrets.toml          ║
║   2. Set "enabled": True in PROVIDER_CONFIG below        ║
║   3. Restart the app                                     ║
╚══════════════════════════════════════════════════════════╝
"""

import streamlit as st
import json
import re
import csv
import io
from datetime import datetime

# ── Sagar AI design system ───────────────────────────────
from sagar_theme import (
    apply_theme, header, card_title, result_block,
    empty_state, status_indicator, highlight_box,
    metric_row, gap_item, footer
)

# ── AI SDK imports (graceful fallback if not installed) ──
try:
    from openai import OpenAI as _OpenAI
    OPENAI_SDK = True
except ImportError:
    OPENAI_SDK = False

try:
    import anthropic as _anthropic
    ANTHROPIC_SDK = True
except ImportError:
    ANTHROPIC_SDK = False

try:
    from google import genai as _google_genai
    GEMINI_SDK = True
except ImportError:
    GEMINI_SDK = False


# ════════════════════════════════════════════════════════
#  PROVIDER CONFIG
#  ─────────────────────────────────────────────────────
#  enabled : False = greyed out / locked in dropdown
#            True  = available to select and use
#  free    : True  = shown with ✅ badge
#            False = shown with 💳 badge
#
#  To unlock Claude or OpenAI later:
#   1. Add API key to .streamlit/secrets.toml
#   2. Change "enabled": False  →  "enabled": True below
#   3. Save and restart the app
# ════════════════════════════════════════════════════════
PROVIDER_CONFIG = {
    "Groq — Llama 3.3 70B": {
        "enabled":  True,
        "free":     True,
        "key_name": "GROQ_API_KEY",
        "key_url":  "console.groq.com",
        "note":     "Free · 14,400 req/day · No credit card needed",
    },
    "Gemini 2.0 Flash — Google": {
        "enabled":  True,
        "free":     True,
        "key_name": "GEMINI_API_KEY",
        "key_url":  "aistudio.google.com/app/apikey",
        "note":     "Free tier · Google account needed",
    },
    "Claude Sonnet — Anthropic": {
        "enabled":  False,          # ← change to True after adding credits
        "free":     False,
        "key_name": "ANTHROPIC_API_KEY",
        "key_url":  "console.anthropic.com",
        "note":     "Paid · Best quality · Enable after adding credits",
    },
    "GPT-4o — OpenAI": {
        "enabled":  False,          # ← change to True after adding credits
        "free":     False,
        "key_name": "OPENAI_API_KEY",
        "key_url":  "platform.openai.com/api-keys",
        "note":     "Paid · Enable after adding credits",
    },
}


# ════════════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Sagar QA — AI Test Case Generator",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_theme()
header("Sagar", "QA", tagline="∿ AI Test Case Generator · By Sagar AI")


# ════════════════════════════════════════════════════════
# SESSION STATE
# ════════════════════════════════════════════════════════
for _key, _default in [
    ("test_cases",       None),
    ("generation_count", 0),
    ("loaded_example",   ""),
]:
    if _key not in st.session_state:
        st.session_state[_key] = _default


# ════════════════════════════════════════════════════════
# CONSTANTS
# ════════════════════════════════════════════════════════
INPUT_TYPES = [
    "User Story",
    "Feature Description",
    "Code Snippet",
    "API Specification",
    "Bug Report",
]

TEST_TYPES = [
    "All Types",
    "Functional Only",
    "Edge Cases Only",
    "Negative Testing",
    "Security Testing",
]

PRIORITY_FILTERS = ["All", "High Only", "Medium Only", "Low Only"]

EXAMPLES = {
    "Login Feature": """As a registered user, I want to log in with my email and password so I can access my account.

Acceptance Criteria:
- Valid email + password → redirect to dashboard
- Wrong password → 'Invalid credentials' error
- Non-existent email → 'Account not found' error
- Account locked after 5 consecutive failed attempts
- 'Remember me' keeps session active for 30 days
- Forgot password link visible on login page
- Password field masked with show/hide toggle""",

    "REST API Endpoint": """POST /api/v1/users/register

Request Body:
{
  "email":    "string (required, valid email format)",
  "password": "string (required, min 8 chars, 1 uppercase, 1 number, 1 special char)",
  "name":     "string (required, 2-50 chars)",
  "phone":    "string (optional, valid E.164 format)"
}

Expected Responses:
  201 - User created { id, email, name, created_at }
  400 - Validation error { field, message }
  409 - Email already registered
  500 - Internal server error""",

    "Search Functionality": """Feature: Product Search

- Search box in global header, available on all pages
- Results load as user types (300ms debounce)
- Each result: image, name, price, rating, stock status
- Filters: category, price range, rating, in-stock only
- Sort: Relevance, Price low-high, Price high-low, Newest
- Show result count: "Showing 24 of 142 results"
- Empty state: "No results for X" + 3 suggested alternatives
- Max 24 results/page with pagination""",

    "Payment Checkout": """Feature: Payment — Cart → Shipping → Payment → Confirmation

Payment methods: Credit/Debit card, UPI, Net Banking

Rules:
- Validate card with Luhn algorithm
- Expiry must not be in the past
- CVV: 3 digits (Visa/Mastercard), 4 digits (Amex)
- Show live order summary throughout
- 30 second timeout during processing
- Success: confirmation page + email receipt
- Failure: show error, allow retry, no double-charge""",
}


# ════════════════════════════════════════════════════════
# AI CALL FUNCTIONS
# ════════════════════════════════════════════════════════

def build_prompts(input_text: str, input_type: str, test_type: str, priority_filter: str):
    system_prompt = """You are a senior QA engineer with 15+ years of experience in software testing.
Generate professional, structured test cases in strict JSON format only.

RULES:
- Respond with ONLY valid JSON — no markdown, no explanation, no preamble
- Each step must be specific and actionable
- Cover happy path, edge cases, and failure scenarios

JSON structure:
{
  "summary": "1-2 sentences describing what was analysed",
  "total_cases": <integer>,
  "test_cases": [
    {
      "id": "TC001",
      "title": "Clear descriptive title",
      "category": "Functional | Edge Case | Negative | Security | Performance | UI/UX",
      "priority": "High | Medium | Low",
      "preconditions": "What must be set up before this test",
      "steps": ["Step 1: action", "Step 2: action"],
      "expected_result": "Exact expected outcome",
      "actual_result": "To be filled during execution",
      "status": "Not Executed",
      "notes": "Optional extra details"
    }
  ],
  "coverage_areas": ["area1", "area2"],
  "missing_requirements": ["any gaps or ambiguities noticed"]
}"""

    type_ctx = {
        "User Story":          "Cover acceptance criteria, happy path, alternate flows, edge cases, and negative scenarios.",
        "Code Snippet":        "Cover unit tests: boundary values, null/empty inputs, type mismatches, exception handling, all logic branches.",
        "Feature Description": "Cover end-to-end flows, integration points, user workflows, UI states, error conditions.",
        "API Specification":   "Cover each endpoint: valid requests, invalid inputs, missing fields, auth, response schema, error codes.",
        "Bug Report":          "Cover regression for the fix, smoke tests for adjacent functionality, edge cases around affected area.",
    }
    test_ctx = {
        "All Types":        "Include Functional, Edge Case, Negative, Security, and Performance cases.",
        "Functional Only":  "Focus only on functional — core workflows and happy path.",
        "Edge Cases Only":  "Focus only on boundary values and unusual but valid inputs.",
        "Negative Testing": "Focus only on invalid inputs, missing data, error handling, failure paths.",
        "Security Testing": "Focus only on security: SQL injection, XSS, auth bypass, privilege escalation, data exposure.",
    }
    priority_ctx = {
        "All":         "Include High, Medium, and Low priority cases.",
        "High Only":   "Include ONLY High priority — critical path and showstoppers.",
        "Medium Only": "Include ONLY Medium priority cases.",
        "Low Only":    "Include ONLY Low priority — cosmetic and nice-to-have checks.",
    }

    user_prompt = f"""Analyse this {input_type} and generate 8-15 professional test cases.

{type_ctx.get(input_type, '')}
{test_ctx.get(test_type, '')}
{priority_ctx.get(priority_filter, '')}

Input:
━━━━━━━━━━━━━━━━
{input_text}
━━━━━━━━━━━━━━━━

Return ONLY the JSON object. No markdown fences."""

    return system_prompt, user_prompt


def call_groq(system_prompt: str, user_prompt: str) -> str:
    key = st.secrets.get("GROQ_API_KEY", "")
    if not key:
        raise ValueError(
            "GROQ_API_KEY not found.\n"
            "1. Go to console.groq.com → sign up free → create API key\n"
            "2. Add to .streamlit/secrets.toml:  GROQ_API_KEY = 'gsk_...'"
        )
    if not OPENAI_SDK:
        raise ImportError("Run: pip install openai")
    client = _OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=4000,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]
    )
    return resp.choices[0].message.content.strip()


def call_gemini(system_prompt: str, user_prompt: str) -> str:
    key = st.secrets.get("GEMINI_API_KEY", "")
    if not key:
        raise ValueError(
            "GEMINI_API_KEY not found.\n"
            "1. Go to aistudio.google.com/app/apikey → create free key\n"
            "2. Add to .streamlit/secrets.toml:  GEMINI_API_KEY = 'AIza...'"
        )
    if not GEMINI_SDK:
        raise ImportError("Run: pip install google-genai")
    client = _google_genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=f"{system_prompt}\n\n---\n\n{user_prompt}",
    )
    return response.text.strip()


def call_claude(system_prompt: str, user_prompt: str) -> str:
    key = st.secrets.get("ANTHROPIC_API_KEY", "")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY not found in secrets.toml")
    if not ANTHROPIC_SDK:
        raise ImportError("Run: pip install anthropic")
    client = _anthropic.Anthropic(api_key=key)
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return msg.content[0].text.strip()


def call_openai(system_prompt: str, user_prompt: str) -> str:
    key = st.secrets.get("OPENAI_API_KEY", "")
    if not key:
        raise ValueError("OPENAI_API_KEY not found in secrets.toml")
    if not OPENAI_SDK:
        raise ImportError("Run: pip install openai")
    client = _OpenAI(api_key=key)
    resp = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=4000,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]
    )
    return resp.choices[0].message.content.strip()


PROVIDER_FN = {
    "Groq — Llama 3.3 70B":      call_groq,
    "Gemini 2.0 Flash — Google": call_gemini,
    "Claude Sonnet — Anthropic": call_claude,
    "GPT-4o — OpenAI":           call_openai,
}


def parse_json(raw: str) -> dict:
    raw = re.sub(r"^```json\s*", "", raw.strip())
    raw = re.sub(r"^```\s*",     "", raw)
    raw = re.sub(r"\s*```$",     "", raw)
    return json.loads(raw)


def generate(input_text, input_type, test_type, priority_filter, provider_name) -> dict:
    system_prompt, user_prompt = build_prompts(input_text, input_type, test_type, priority_filter)
    fn = PROVIDER_FN.get(provider_name)
    if not fn:
        raise ValueError(f"Unknown provider: {provider_name}")
    return parse_json(fn(system_prompt, user_prompt))


# ════════════════════════════════════════════════════════
# EXPORT HELPERS
# ════════════════════════════════════════════════════════

def to_markdown(data: dict) -> str:
    tcs = data.get("test_cases", [])
    ts  = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# Sagar QA — Test Cases Export",
        f"*Generated: {ts} · Total: {len(tcs)} cases*\n",
        f"**Summary:** {data.get('summary', '')}\n",
        "---\n",
    ]
    for tc in tcs:
        lines += [
            f"## {tc.get('id','')} — {tc.get('title','')}",
            f"**Category:** {tc.get('category','')}  "
            f"| **Priority:** {tc.get('priority','')}  "
            f"| **Status:** {tc.get('status','Not Executed')}\n",
            f"**Preconditions:** {tc.get('preconditions','')}\n",
            "**Steps:**",
        ]
        for i, s in enumerate(tc.get("steps", []), 1):
            lines.append(f"{i}. {s}")
        lines += [
            f"\n**Expected Result:** {tc.get('expected_result','')}",
            f"**Actual Result:** {tc.get('actual_result','To be filled')}",
        ]
        if tc.get("notes"):
            lines.append(f"**Notes:** {tc['notes']}")
        lines.append("\n---\n")
    if data.get("coverage_areas"):
        lines.append("## Coverage Areas")
        for a in data["coverage_areas"]:
            lines.append(f"- {a}")
    if data.get("missing_requirements"):
        lines.append("\n## Gaps & Ambiguities")
        for g in data["missing_requirements"]:
            lines.append(f"- ⚠ {g}")
    return "\n".join(lines)


def to_csv(data: dict) -> str:
    out = io.StringIO()
    w   = csv.writer(out)
    w.writerow(["ID","Title","Category","Priority","Preconditions",
                "Steps","Expected Result","Actual Result","Status","Notes"])
    for tc in data.get("test_cases", []):
        w.writerow([
            tc.get("id",""), tc.get("title",""), tc.get("category",""),
            tc.get("priority",""), tc.get("preconditions",""),
            " | ".join(tc.get("steps",[])), tc.get("expected_result",""),
            tc.get("actual_result",""), tc.get("status",""), tc.get("notes",""),
        ])
    return out.getvalue()


# ════════════════════════════════════════════════════════
# LAYOUT
# ════════════════════════════════════════════════════════
col_left, col_right = st.columns([1, 1.2], gap="large")


# ── LEFT PANEL ───────────────────────────────────────────
with col_left:

    card_title("∿ Input")

    input_type = st.selectbox(
        "What are you pasting?", INPUT_TYPES,
        help="Sagar QA adapts the AI prompt based on your input type."
    )

    input_text = st.text_area(
        "Paste your user story, code, or feature here",
        height=250,
        placeholder=(
            "As a registered user, I want to log in with email and password.\n\n"
            "Acceptance Criteria:\n"
            "- Valid credentials → redirect to dashboard\n"
            "- Wrong password → show error\n"
            "- Locked after 5 failed attempts"
        ),
    )

    # ── AI Provider selector ─────────────────────────────
    card_title("∿ AI Provider", margin_top=True)

    # Build labelled options — enabled first, locked appended after
    enabled_options  = []
    disabled_options = []

    for name, cfg in PROVIDER_CONFIG.items():
        badge = "✅ Free" if cfg["free"] else "💳 Paid"
        if cfg["enabled"]:
            enabled_options.append((f"{badge}  ·  {name}", name, cfg))
        else:
            disabled_options.append((f"🔒 Locked  ·  {name}", name, cfg))

    all_display   = [o[0] for o in enabled_options + disabled_options]
    all_names     = [o[1] for o in enabled_options + disabled_options]
    all_cfgs      = [o[2] for o in enabled_options + disabled_options]

    selected_idx = st.selectbox(
        "Choose AI provider",
        range(len(all_display)),
        format_func=lambda i: all_display[i],
        index=0,
        help="🔒 Locked = requires paid API key. See README to unlock."
    )

    provider_name = all_names[selected_idx]
    cfg           = all_cfgs[selected_idx]
    is_locked     = not cfg["enabled"]

    # Status panel below dropdown
    if is_locked:
        st.markdown(f"""
<div style="background:rgba(248,113,113,0.07);border:1px solid rgba(248,113,113,0.22);
            border-left:3px solid #f87171;border-radius:0 2px 2px 0;
            padding:0.8rem 1rem;margin-bottom:0.8rem;">
  <div style="color:#f87171;font-weight:600;margin-bottom:4px;font-size:0.88rem;">
    🔒 Provider Locked
  </div>
  <div style="color:#cbd5e1;font-size:0.84rem;margin-bottom:6px;">
    {cfg.get('note', 'Requires a paid API key.')}
  </div>
  <div style="font-family:'DM Mono',monospace;font-size:0.63rem;color:#7baab8;line-height:1.7;">
    To unlock:<br>
    1. Get key → <a href="https://{cfg.get('key_url','')}" target="_blank"
       style="color:#f87171;">{cfg.get('key_url','')}</a><br>
    2. Add <b style="color:#f0f8ff;">{cfg.get('key_name','')}</b> to secrets.toml<br>
    3. Set <b style="color:#f0f8ff;">enabled: True</b> in PROVIDER_CONFIG in app.py
  </div>
</div>
""", unsafe_allow_html=True)
    else:
        key_name   = cfg.get("key_name", "")
        key_url    = cfg.get("key_url", "")
        key_is_set = bool(st.secrets.get(key_name, ""))
        status_indicator(key_name, key_is_set, key_url)
        st.markdown(
            f'<div style="font-family:\'DM Mono\',monospace;font-size:0.62rem;'
            f'color:#7baab8;margin-top:-6px;margin-bottom:8px;">'
            f'{cfg.get("note","")}</div>',
            unsafe_allow_html=True
        )

    # ── Options ──────────────────────────────────────────
    card_title("∿ Options", margin_top=True)

    c1, c2 = st.columns(2)
    with c1:
        test_type = st.selectbox("Test focus", TEST_TYPES)
    with c2:
        priority = st.selectbox("Priority filter", PRIORITY_FILTERS)

    st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

    generate_btn = st.button(
        "⬡  Generate Test Cases",
        type="primary",
        disabled=is_locked,
    )

    if is_locked:
        st.markdown(
            '<div style="text-align:center;font-size:0.78rem;color:#f87171;margin-top:4px;">'
            '↑ Select a free provider (Groq or Gemini) to generate</div>',
            unsafe_allow_html=True
        )

    # ── Examples ─────────────────────────────────────────
    with st.expander("📋 Load a built-in example"):
        ex_key = st.selectbox("Choose an example", list(EXAMPLES.keys()))
        if st.button("Load this example →"):
            st.session_state.loaded_example = EXAMPLES[ex_key]
            st.rerun()

    if st.session_state.loaded_example:
        highlight_box(
            "✓ Example loaded",
            "Copy the text below into the input box, then click Generate.<br><br>"
            f'<code style="font-size:0.76rem;opacity:0.75;">'
            f'{st.session_state.loaded_example[:100].replace(chr(10)," ")}...</code>'
        )
        if st.button("Clear example"):
            st.session_state.loaded_example = ""
            st.rerun()


# ── RIGHT PANEL ──────────────────────────────────────────
with col_right:

    if generate_btn:
        final_text = (input_text or st.session_state.loaded_example or "").strip()

        if not final_text:
            st.error("Please paste your input on the left, or load a built-in example.")
        elif len(final_text) < 20:
            st.error("Input is too short. Please provide more detail.")
        else:
            key_name   = cfg.get("key_name", "")
            key_is_set = bool(st.secrets.get(key_name, ""))
            if not key_is_set:
                st.error(
                    f"No API key found for **{provider_name}**. "
                    f"Add `{key_name}` to `.streamlit/secrets.toml` and restart."
                )
            else:
                with st.spinner(f"∿ Generating with {provider_name}..."):
                    try:
                        data = generate(final_text, input_type, test_type, priority, provider_name)
                        st.session_state.test_cases       = data
                        st.session_state.generation_count += 1
                    except json.JSONDecodeError:
                        st.error("AI returned unexpected format. Please try again.")
                    except ValueError as e:
                        st.error(str(e))
                    except Exception as e:
                        st.error(f"Something went wrong: {e}")

    if st.session_state.test_cases:
        data = st.session_state.test_cases
        tcs  = data.get("test_cases", [])
        high = sum(1 for t in tcs if t.get("priority") == "High")
        cats = len(set(t.get("category", "") for t in tcs))

        metric_row([
            {"value": str(len(tcs)), "label": "Test Cases"},
            {"value": str(high),     "label": "High Priority"},
            {"value": str(cats),     "label": "Categories"},
            {"value": f"#{st.session_state.generation_count}", "label": "Run"},
        ])

        st.markdown("---")

        if data.get("summary"):
            highlight_box("∿ Analysis Summary", data["summary"])

        tab_all, tab_high, tab_edge, tab_export = st.tabs([
            f"All Cases ({len(tcs)})",
            f"High Priority ({high})",
            "Edge & Negative",
            "Export",
        ])

        def show_cases(cases):
            if not cases:
                empty_state("◎", "No cases in this filter", "Try 'All Cases' tab")
                return
            for tc in cases:
                result_block(tc)

        with tab_all:
            show_cases(tcs)
        with tab_high:
            show_cases([t for t in tcs if t.get("priority") == "High"])
        with tab_edge:
            show_cases([t for t in tcs if t.get("category") in ["Edge Case","Negative","Security"]])
        with tab_export:
            card_title("∿ Download Your Test Cases")
            e1, e2 = st.columns(2)
            ts = datetime.now().strftime("%Y%m%d_%H%M")
            with e1:
                st.download_button("⬇ Markdown (.md)", to_markdown(data),
                    f"sagarqa_{ts}.md", "text/markdown")
            with e2:
                st.download_button("⬇ CSV (.csv)", to_csv(data),
                    f"sagarqa_{ts}.csv", "text/csv")
            if data.get("missing_requirements"):
                card_title("∿ Gaps Detected", margin_top=True)
                for g in data["missing_requirements"]:
                    gap_item(g)
            if data.get("coverage_areas"):
                card_title("∿ Coverage Areas", margin_top=True)
                cols = st.columns(2)
                for i, area in enumerate(data["coverage_areas"]):
                    cols[i % 2].markdown(
                        f'<div style="font-size:0.82rem;color:#14b8a6;padding:3px 0;">✓ {area}</div>',
                        unsafe_allow_html=True
                    )
    else:
        empty_state(
            "⬡",
            "Your test cases will appear here",
            "Paste input on the left → Click Generate"
        )


# ════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════
footer()
