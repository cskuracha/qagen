# ⬡ Sagar QA — AI Test Case Generator
### Part of **Sagar AI** · *AI That Runs Deep*

> Built by C.S. Sagar — 15 years in software testing, tired of writing test cases by hand.

---

## 📁 Project Structure

```
SagarAI-Final/
│
├── app.py                          ← Main Streamlit app (run this)
├── sagar_theme.py                  ← Sagar AI design system (reuse in all apps)
├── requirements.txt                ← Python dependencies
├── Dockerfile                      ← Docker build for VPS / cloud
├── docker-compose.yml              ← Easy Docker deployment
├── .gitignore                      ← Keeps secrets out of git
│
├── .streamlit/
│   ├── config.toml                 ← Streamlit theme config
│   └── secrets.toml.example        ← API key template (copy → secrets.toml)
│
└── flask/                          ← Flask/Django UI template system
    ├── templates/
    │   ├── base.html               ← Base layout (extend in every Flask page)
    │   └── qa.html                 ← Example QA page
    └── static/
        ├── css/sagar-ui.css        ← Full CSS design system
        └── js/sagar-ui.js          ← Tabs, alerts, loading, download helpers
```

---

## 🚀 Option 1 — Run Locally (Fastest)

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Add your API key
```bash
# Copy the example file
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit secrets.toml and paste your real key
# You only need ONE key to start
```

### Step 3: Run
```bash
streamlit run app.py
```
Open **http://localhost:8501** in your browser. That's it. ✓

---

## ☁️ Option 2 — Deploy on Streamlit Community Cloud (Free, Recommended)

**Deploy in under 5 minutes:**

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Sagar QA MVP"
git remote add origin https://github.com/YOUR_USERNAME/sagarqa.git
git push -u origin main
```
> ⚠ Make sure `.gitignore` is committed so `secrets.toml` is never pushed.

### Step 2: Deploy
1. Go to **https://share.streamlit.io**
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repo → Branch: `main` → File: `app.py`
5. Click **"Advanced settings"** → **Secrets** → paste:
```toml
ANTHROPIC_API_KEY = "sk-ant-your-real-key"
```
6. Click **Deploy** → live in ~2 minutes at `https://your-app.streamlit.app`

---

## 🐳 Option 3 — Deploy with Docker (Hostinger VPS or any server)

### Step 1: On your server, install Docker
```bash
curl -fsSL https://get.docker.com | sh
```

### Step 2: Clone and build
```bash
git clone https://github.com/YOUR_USERNAME/sagarqa.git
cd sagarqa
```

### Step 3: Set API keys and run
```bash
# Method A: pass keys directly
docker run -d -p 8501:8501 \
  -e ANTHROPIC_API_KEY=sk-ant-your-key \
  --name sagarqa \
  --restart unless-stopped \
  $(docker build -q .)

# Method B: use docker-compose (cleaner)
# Create a .env file:
echo "ANTHROPIC_API_KEY=sk-ant-your-key" > .env
docker-compose up -d --build
```

### Step 4: Access your app
- Local:        `http://localhost:8501`
- Hostinger VPS: `http://YOUR_VPS_IP:8501`
- With domain:  Set up Nginx reverse proxy (see below)

### Optional: Nginx reverse proxy (custom domain)
```nginx
server {
    listen 80;
    server_name sagarqa.yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

---

## 🔑 Getting API Keys

| Provider | Free Tier | Get Key |
|---|---|---|
| **Claude (Anthropic)** | Yes — limited | https://console.anthropic.com |
| **GPT-4o (OpenAI)** | $5 credit on signup | https://platform.openai.com/api-keys |
| **Gemini 1.5 Pro (Google)** | Generous free tier | https://aistudio.google.com/app/apikey |

You only need **one key** to start. Add all three later to let users choose.

---

## ✨ Features

| Feature | Details |
|---|---|
| 3 AI Providers | Claude, GPT-4o, Gemini — switch with a dropdown |
| 5 Input Types | User Story, Feature Description, Code, API Spec, Bug Report |
| 5 Test Focuses | All Types, Functional, Edge Cases, Negative, Security |
| Priority Filter | All / High / Medium / Low |
| Tabbed Results | All Cases / High Priority / Edge & Negative |
| Export | Markdown (.md) + CSV (.csv) |
| Gap Detection | AI flags missing requirements in your input |
| Built-in Examples | Login, REST API, Search, Payment — try instantly |
| Reusable Theme | sagar_theme.py — drop into any Sagar AI app |

---

## 🎨 Reusing the Design System

### For your next Streamlit app (Sagar Calm, Sagar Agro, etc.)

Copy `sagar_theme.py` into your new project, then:

```python
import streamlit as st
from sagar_theme import apply_theme, header, card_title, footer

st.set_page_config(page_title="Sagar Calm", page_icon="◎", layout="wide")

apply_theme()                                              # Full theme — 1 line
header("Sagar", "Calm", tagline="∿ AI Burnout Companion") # Branded header

card_title("∿ How are you feeling today?")
# ... your app content ...

footer()
```

### To retheme all apps at once
Edit the `THEME` dict at the top of `sagar_theme.py`:
```python
THEME = {
    "primary":   "#0d9488",  # change teal to any colour
    "bg":        "#020b18",  # change background
    ...
}
```

### For Flask / Django apps
Use `flask/static/css/sagar-ui.css` and `flask/static/js/sagar-ui.js`.
Extend `flask/templates/base.html` in every page.

---

## 💰 Adding Payments (Next Step)

To charge users, add Razorpay (India) or Stripe (Global):

```python
# In app.py, add usage tracking in session_state
if st.session_state.generation_count >= 5 and not is_pro_user():
    st.warning("Free limit reached. Upgrade to Pro for unlimited generations.")
    st.markdown("[Upgrade to Sagar QA Pro →](https://razorpay.com/your-payment-link)")
    st.stop()
```

**Pricing recommendation:**
- Free: 5 generations/day
- Pro: ₹799/month — unlimited

---

## 🗺 Roadmap

```
✅ Sagar QA     — AI test case generator (this app — done!)
⏳ Sagar Calm   — AI burnout companion for IT professionals
🔜 Sagar Agro   — ML crop intelligence for South India
```

---

*Sagar AI · AI That Runs Deep · Built by C.S. Sagar · © 2025*
