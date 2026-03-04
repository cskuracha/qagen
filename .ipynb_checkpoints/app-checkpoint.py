import streamlit as st
import anthropic
import json
import re
from datetime import datetime

# ── Page config ─────────────────────────────────────────
st.set_page_config(
    page_title="Sagar QA — AI Test Case Generator",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ───────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300&family=DM+Mono:wght@300;400;500&family=Outfit:wght@200;300;400;500;600&display=swap');

/* Reset & Base */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background: #020b18;
    color: #f0f8ff;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px; }

/* ── HEADER ── */
.sagar-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 2rem;
}
.sagar-logo {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.8rem;
    font-weight: 300;
    letter-spacing: 0.1em;
    color: #f0f8ff;
    margin-bottom: 0.3rem;
}
.sagar-logo span { color: #14b8a6; font-style: italic; }
.sagar-tagline {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.3em;
    color: #0d9488;
    text-transform: uppercase;
}

/* ── CARDS ── */
.card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 2px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.card-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: #0d9488;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* ── INPUT AREA ── */
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 2px !important;
    color: #f0f8ff !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: rgba(20,184,166,0.5) !important;
    box-shadow: 0 0 0 1px rgba(20,184,166,0.2) !important;
}
.stTextArea label {
    color: #7baab8 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.85rem !important;
}

/* ── SELECT BOX ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 2px !important;
    color: #f0f8ff !important;
}
.stSelectbox label {
    color: #7baab8 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.85rem !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: #0d9488 !important;
    color: #020b18 !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #14b8a6 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: rgba(13,148,136,0.1) !important;
    color: #14b8a6 !important;
    border: 1px solid rgba(20,184,166,0.3) !important;
    border-radius: 2px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    background: rgba(13,148,136,0.2) !important;
    border-color: #14b8a6 !important;
}

/* ── RADIO ── */
.stRadio label {
    color: #7baab8 !important;
    font-size: 0.85rem !important;
}
.stRadio > div { gap: 0.5rem; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.02) !important;
    border-bottom: 1px solid rgba(255,255,255,0.07) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #7baab8 !important;
    background: transparent !important;
    border: none !important;
    padding: 0.8rem 1.5rem !important;
}
.stTabs [aria-selected="true"] {
    color: #14b8a6 !important;
    border-bottom: 2px solid #14b8a6 !important;
}

/* ── METRICS ── */
.stMetric {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 2px !important;
    padding: 1rem !important;
}
.stMetric label { color: #7baab8 !important; font-size: 0.75rem !important; }
.stMetric [data-testid="metric-container"] div { color: #14b8a6 !important; }

/* ── TEST CASE OUTPUT ── */
.test-case-block {
    background: rgba(13,148,136,0.04);
    border: 1px solid rgba(20,184,166,0.15);
    border-left: 3px solid #0d9488;
    border-radius: 0 2px 2px 0;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    font-family: 'Outfit', sans-serif;
}
.tc-id {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: #0d9488;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.tc-title {
    font-size: 1rem;
    font-weight: 600;
    color: #f0f8ff;
    margin-bottom: 0.8rem;
}
.tc-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    color: #7baab8;
    text-transform: uppercase;
    margin-top: 0.6rem;
    margin-bottom: 0.2rem;
}
.tc-content { font-size: 0.88rem; color: #cbd5e1; line-height: 1.6; }
.tc-priority-high   { color: #f87171; font-weight: 600; }
.tc-priority-medium { color: #fbbf24; font-weight: 600; }
.tc-priority-low    { color: #34d399; font-weight: 600; }

/* ── SPINNER ── */
.stSpinner > div { border-top-color: #14b8a6 !important; }

/* ── DIVIDER ── */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* ── INFO / WARNING ── */
.stAlert {
    background: rgba(13,148,136,0.08) !important;
    border: 1px solid rgba(20,184,166,0.2) !important;
    color: #a8d8d0 !important;
    border-radius: 2px !important;
}

/* ── SIDEBAR ── */
.css-1d391kg { background: #030d1a !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #020b18; }
::-webkit-scrollbar-thumb { background: rgba(13,148,136,0.4); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #0d9488; }

/* ── COUNTER BADGE ── */
.badge {
    display: inline-block;
    background: rgba(13,148,136,0.15);
    border: 1px solid rgba(20,184,166,0.3);
    color: #14b8a6;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    padding: 2px 10px;
    border-radius: 20px;
    margin-left: 8px;
}

/* ── WAVE DECORATION ── */
.wave-line {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: rgba(13,148,136,0.3);
    letter-spacing: 0.1em;
    text-align: center;
    padding: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Header ───────────────────────────────────────────────
st.markdown("""
<div class="sagar-header">
    <div class="sagar-logo">Sagar<span>QA</span></div>
    <div class="sagar-tagline">∿ AI Test Case Generator · By Sagar AI</div>
</div>
""", unsafe_allow_html=True)


# ── Session state ────────────────────────────────────────
if "test_cases" not in st.session_state:
    st.session_state.test_cases = None
if "raw_output" not in st.session_state:
    st.session_state.raw_output = None
if "generation_count" not in st.session_state:
    st.session_state.generation_count = 0
if "last_input" not in st.session_state:
    st.session_state.last_input = ""


# ── AI Generation ────────────────────────────────────────
def generate_test_cases(input_text, input_type, test_type, priority_filter):
    """Call Claude API to generate structured test cases."""

    system_prompt = """You are an expert QA engineer with 15+ years of experience in software testing. 
You generate comprehensive, professional test cases in strict JSON format.

Always respond with ONLY a valid JSON object — no markdown, no explanation, no preamble.

JSON structure:
{
  "summary": "brief summary of what was analyzed",
  "total_cases": <number>,
  "test_cases": [
    {
      "id": "TC001",
      "title": "descriptive test case title",
      "category": "Functional|Edge Case|Negative|Security|Performance|UI/UX",
      "priority": "High|Medium|Low",
      "preconditions": "what must be true before running this test",
      "steps": ["step 1", "step 2", "step 3"],
      "expected_result": "what should happen",
      "actual_result": "To be filled during execution",
      "status": "Not Executed",
      "notes": "any additional notes or considerations"
    }
  ],
  "coverage_areas": ["area1", "area2"],
  "missing_requirements": ["any gaps or ambiguities noticed"]
}"""

    type_context = {
        "User Story": "This is a user story. Generate test cases that cover the acceptance criteria, happy path, edge cases, and negative scenarios.",
        "Code Snippet": "This is a code snippet. Generate test cases for unit testing, boundary values, null/empty inputs, exception handling, and logic paths.",
        "Feature Description": "This is a feature description. Generate end-to-end test cases, integration scenarios, user workflows, and error conditions.",
        "API Specification": "This is an API specification. Generate test cases for each endpoint: valid requests, invalid inputs, auth scenarios, response validation, and error codes.",
        "Bug Report": "This is a bug report. Generate regression test cases to verify the fix, related scenarios that might be affected, and edge cases around this area."
    }

    test_type_context = {
        "All Types": "Include all types: Functional, Edge Cases, Negative, Security, Performance.",
        "Functional Only": "Focus on functional test cases — happy path and core workflows.",
        "Edge Cases Only": "Focus on boundary values, edge cases, and unusual inputs.",
        "Negative Testing": "Focus on negative test cases — invalid inputs, error handling, failure scenarios.",
        "Security Testing": "Focus on security test cases — injection, auth bypass, data exposure, etc."
    }

    user_prompt = f"""Analyze the following {input_type} and generate professional test cases.

{type_context.get(input_type, '')}
{test_type_context.get(test_type, '')}

Priority filter: {priority_filter} (if not 'All', only include cases of this priority level)

Input to analyze:
---
{input_text}
---

Generate between 8 and 15 test cases. Be specific, actionable, and thorough.
Return ONLY the JSON object."""

    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": user_prompt}],
        system=system_prompt
    )

    raw = message.content[0].text.strip()

    # Clean any accidental markdown fences
    raw = re.sub(r'^```json\s*', '', raw)
    raw = re.sub(r'^```\s*', '', raw)
    raw = re.sub(r'\s*```$', '', raw)

    return json.loads(raw), raw


def export_to_markdown(test_cases_data):
    """Convert test cases to a markdown string for download."""
    lines = []
    lines.append(f"# Sagar QA — Test Cases Export")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    lines.append(f"**Summary:** {test_cases_data.get('summary', '')}\n")
    lines.append(f"**Total Cases:** {test_cases_data.get('total_cases', 0)}\n")
    lines.append("---\n")

    for tc in test_cases_data.get("test_cases", []):
        lines.append(f"## {tc['id']} — {tc['title']}")
        lines.append(f"**Category:** {tc['category']}  |  **Priority:** {tc['priority']}  |  **Status:** {tc['status']}\n")
        lines.append(f"**Preconditions:** {tc['preconditions']}\n")
        lines.append("**Steps:**")
        for i, step in enumerate(tc.get("steps", []), 1):
            lines.append(f"{i}. {step}")
        lines.append(f"\n**Expected Result:** {tc['expected_result']}")
        lines.append(f"**Actual Result:** {tc['actual_result']}")
        if tc.get("notes"):
            lines.append(f"**Notes:** {tc['notes']}")
        lines.append("\n---\n")

    if test_cases_data.get("coverage_areas"):
        lines.append("## Coverage Areas")
        for area in test_cases_data["coverage_areas"]:
            lines.append(f"- {area}")

    if test_cases_data.get("missing_requirements"):
        lines.append("\n## Gaps & Ambiguities Noticed")
        for gap in test_cases_data["missing_requirements"]:
            lines.append(f"- {gap}")

    return "\n".join(lines)


def export_to_csv(test_cases_data):
    """Convert test cases to CSV string."""
    import csv
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Title", "Category", "Priority", "Preconditions", "Steps", "Expected Result", "Actual Result", "Status", "Notes"])
    for tc in test_cases_data.get("test_cases", []):
        writer.writerow([
            tc.get("id", ""),
            tc.get("title", ""),
            tc.get("category", ""),
            tc.get("priority", ""),
            tc.get("preconditions", ""),
            " | ".join(tc.get("steps", [])),
            tc.get("expected_result", ""),
            tc.get("actual_result", ""),
            tc.get("status", ""),
            tc.get("notes", "")
        ])
    return output.getvalue()


# ── MAIN LAYOUT ──────────────────────────────────────────
col_left, col_right = st.columns([1, 1.2], gap="large")

# ─── LEFT: Input Panel ───────────────────────────────────
with col_left:
    st.markdown('<div class="card-title">∿ Input</div>', unsafe_allow_html=True)

    input_type = st.selectbox(
        "What are you pasting?",
        ["User Story", "Feature Description", "Code Snippet", "API Specification", "Bug Report"],
        help="Tell Sagar QA what kind of input you're providing for best results"
    )

    input_text = st.text_area(
        "Paste your user story, code, or feature description",
        height=280,
        placeholder="""Example User Story:
As a registered user,
I want to log into my account using email and password,
So that I can access my personal dashboard.

Acceptance Criteria:
- Valid credentials → redirect to dashboard
- Invalid password → show error message
- Account locked after 5 failed attempts
- 'Remember me' checkbox persists session for 30 days""",
        key="input_text"
    )

    st.markdown('<div class="card-title" style="margin-top:1rem">∿ Options</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        test_type = st.selectbox(
            "Test type focus",
            ["All Types", "Functional Only", "Edge Cases Only", "Negative Testing", "Security Testing"]
        )
    with col_b:
        priority_filter = st.selectbox(
            "Priority filter",
            ["All", "High Only", "Medium Only", "Low Only"]
        )

    generate_btn = st.button("⬡  Generate Test Cases", type="primary")

    # Example loader
    with st.expander("📋 Load an example input"):
        ex = st.selectbox("Choose example", [
            "Login Feature",
            "REST API Endpoint",
            "Search Functionality",
            "Payment Flow"
        ])
        if st.button("Load Example", key="load_ex"):
            examples = {
                "Login Feature": """As a registered user, I want to log in with my email and password so I can access my account.

Acceptance Criteria:
- Valid email + password → redirect to dashboard
- Wrong password → 'Invalid credentials' error
- Non-existent email → 'Account not found' error  
- Account locked after 5 failed attempts
- Remember me checkbox keeps session for 30 days
- Forgot password link visible on login page""",
                "REST API Endpoint": """POST /api/v1/users/register

Request body:
{
  "email": "string (required, valid email format)",
  "password": "string (required, min 8 chars, 1 uppercase, 1 number)",
  "name": "string (required, 2-50 chars)",
  "phone": "string (optional, valid phone format)"
}

Responses:
- 201: User created successfully
- 400: Validation error with field details
- 409: Email already registered
- 500: Internal server error""",
                "Search Functionality": """Feature: Product Search

Users can search for products by name, category, or keyword.
- Search box in header, available on all pages
- Results appear as user types (debounced 300ms)
- Show product name, price, image, and rating
- Filter by category, price range, and rating
- Sort by relevance, price (low-high, high-low), newest
- Show 'No results found' with suggestions if empty
- Maximum 50 results per page with pagination""",
                "Payment Flow": """Feature: Checkout Payment

User selects items → goes to checkout → enters payment details → confirms order.

Payment methods: Credit card, Debit card, UPI, Net Banking
- Card: validate number (Luhn), expiry (not past), CVV (3-4 digits)
- UPI: validate UPI ID format
- Show order summary before payment
- Loading state during payment processing
- Success: show order confirmation + send email
- Failure: show error, allow retry, don't charge twice
- Timeout after 30 seconds"""
            }
            st.session_state.last_input = examples[ex]
            st.rerun()

    if st.session_state.last_input:
        st.info(f"✓ Example loaded — '{ex}' is ready in the text area above. Paste it manually or click Generate.")


# ─── RIGHT: Output Panel ─────────────────────────────────
with col_right:
    # Generate on button click
    if generate_btn:
        final_input = input_text.strip() or st.session_state.last_input.strip()
        if not final_input:
            st.error("Please paste your user story, code, or feature description first.")
        elif len(final_input) < 20:
            st.error("Input is too short. Please provide more detail for better test cases.")
        else:
            with st.spinner("∿  Sagar QA is analysing your input..."):
                try:
                    result, raw = generate_test_cases(
                        final_input, input_type, test_type, priority_filter
                    )
                    st.session_state.test_cases = result
                    st.session_state.raw_output = raw
                    st.session_state.generation_count += 1
                except json.JSONDecodeError:
                    st.error("Received an unexpected response. Please try again.")
                except anthropic.AuthenticationError:
                    st.error("API key error. Please check your ANTHROPIC_API_KEY in secrets.")
                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")

    # Show results
    if st.session_state.test_cases:
        data = st.session_state.test_cases
        tcs  = data.get("test_cases", [])

        # ── Metrics row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Test Cases", len(tcs))
        high_count = sum(1 for t in tcs if t.get("priority") == "High")
        m2.metric("High Priority", high_count)
        categories = len(set(t.get("category", "") for t in tcs))
        m3.metric("Categories", categories)
        m4.metric("Generated", f"#{st.session_state.generation_count}")

        st.markdown("---")

        # ── Summary
        if data.get("summary"):
            st.markdown(f"""
            <div style="background:rgba(13,148,136,0.06);border:1px solid rgba(20,184,166,0.15);
                        border-radius:2px;padding:1rem 1.2rem;margin-bottom:1rem;">
                <div class="card-title">∿ Analysis Summary</div>
                <div style="font-size:0.9rem;color:#cbd5e1;line-height:1.6;">{data['summary']}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Tabs
        tab_all, tab_high, tab_edge, tab_export = st.tabs([
            f"All Cases ({len(tcs)})",
            f"High Priority ({high_count})",
            "Edge & Negative",
            "Export"
        ])

        def render_test_cases(cases):
            if not cases:
                st.markdown('<div style="color:#7baab8;font-size:0.85rem;padding:1rem 0;">No test cases in this filter.</div>', unsafe_allow_html=True)
                return
            for tc in cases:
                priority_class = {
                    "High": "tc-priority-high",
                    "Medium": "tc-priority-medium",
                    "Low": "tc-priority-low"
                }.get(tc.get("priority", ""), "tc-priority-low")

                steps_html = "".join(f'<div style="margin:3px 0;color:#94a3b8;font-size:0.85rem;">  {i+1}. {s}</div>'
                                     for i, s in enumerate(tc.get("steps", [])))

                st.markdown(f"""
                <div class="test-case-block">
                    <div class="tc-id">{tc.get('id','TC')} · {tc.get('category','')}</div>
                    <div class="tc-title">{tc.get('title','')}</div>
                    <div style="margin-bottom:0.6rem;">
                        <span class="{priority_class}">● {tc.get('priority','')}</span>
                        <span style="color:#475569;font-size:0.8rem;margin-left:1rem;">Status: {tc.get('status','')}</span>
                    </div>
                    <div class="tc-label">Preconditions</div>
                    <div class="tc-content">{tc.get('preconditions','—')}</div>
                    <div class="tc-label">Test Steps</div>
                    {steps_html}
                    <div class="tc-label">Expected Result</div>
                    <div class="tc-content" style="color:#86efac;">{tc.get('expected_result','')}</div>
                    {f'<div class="tc-label">Notes</div><div class="tc-content" style="color:#94a3b8;font-style:italic;">{tc.get("notes","")}</div>' if tc.get('notes') else ''}
                </div>
                """, unsafe_allow_html=True)

        with tab_all:
            render_test_cases(tcs)

        with tab_high:
            high_cases = [t for t in tcs if t.get("priority") == "High"]
            render_test_cases(high_cases)

        with tab_edge:
            edge_cases = [t for t in tcs if t.get("category") in ["Edge Case", "Negative", "Security"]]
            render_test_cases(edge_cases)

        with tab_export:
            st.markdown('<div class="card-title">∿ Export Your Test Cases</div>', unsafe_allow_html=True)
            st.markdown('<div style="color:#7baab8;font-size:0.85rem;margin-bottom:1rem;">Download in your preferred format.</div>', unsafe_allow_html=True)

            ex_col1, ex_col2 = st.columns(2)
            with ex_col1:
                md_content = export_to_markdown(data)
                st.download_button(
                    "⬇ Download as Markdown (.md)",
                    data=md_content,
                    file_name=f"sagarqa_test_cases_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                    mime="text/markdown"
                )
            with ex_col2:
                csv_content = export_to_csv(data)
                st.download_button(
                    "⬇ Download as CSV (.csv)",
                    data=csv_content,
                    file_name=f"sagarqa_test_cases_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )

            if data.get("missing_requirements"):
                st.markdown('<div class="card-title" style="margin-top:1.5rem;">∿ Gaps & Ambiguities Detected</div>', unsafe_allow_html=True)
                for gap in data["missing_requirements"]:
                    st.markdown(f'<div style="font-size:0.85rem;color:#fbbf24;padding:4px 0;">⚠ {gap}</div>', unsafe_allow_html=True)

            if data.get("coverage_areas"):
                st.markdown('<div class="card-title" style="margin-top:1rem;">∿ Coverage Areas</div>', unsafe_allow_html=True)
                cols = st.columns(2)
                for i, area in enumerate(data["coverage_areas"]):
                    cols[i % 2].markdown(f'<div style="font-size:0.82rem;color:#14b8a6;padding:3px 0;">✓ {area}</div>', unsafe_allow_html=True)

    else:
        # Empty state
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem;border:1px dashed rgba(255,255,255,0.07);border-radius:2px;">
            <div style="font-size:2.5rem;margin-bottom:1rem;opacity:0.3;">⬡</div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;font-weight:300;
                        color:#7baab8;margin-bottom:0.5rem;">Your test cases will appear here</div>
            <div style="font-family:'DM Mono',monospace;font-size:0.65rem;letter-spacing:0.2em;
                        color:rgba(123,170,184,0.4);text-transform:uppercase;">
                Paste input → Select type → Generate
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;padding:1rem 0;">
    <div style="font-family:'DM Mono',monospace;font-size:0.62rem;letter-spacing:0.2em;
                color:rgba(123,170,184,0.35);text-transform:uppercase;">
        ∿ Sagar AI · AI That Runs Deep · Built by C.S. Sagar
    </div>
</div>
""", unsafe_allow_html=True)
