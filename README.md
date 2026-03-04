# ⬡ Sagar QA — AI Test Case Generator

> **By Sagar AI** · AI That Runs Deep

An AI-powered test case generator built for QA engineers. Paste a user story, code snippet, feature description, or API spec — and get structured, professional test cases in seconds.

---

## 🚀 Deploy in 5 Minutes (Streamlit Community Cloud)

### Step 1 — Push to GitHub
```bash
# Create a new repo on github.com, then:
git init
git add .
git commit -m "Initial Sagar QA MVP"
git remote add origin https://github.com/YOUR_USERNAME/sagar-qa.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Community Cloud
1. Go to **https://share.streamlit.io**
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repo → Branch: `main` → Main file: `app.py`
5. Click **"Advanced settings"** → Add your secret:
   ```
   ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
   ```
6. Click **Deploy** — your app will be live in ~2 minutes!

### Step 3 — Get your API Key
1. Go to **https://console.anthropic.com**
2. Sign up / log in
3. Go to **API Keys** → Create a new key
4. Copy and paste into Streamlit secrets

---

## 🖥️ Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Add your API key
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml and add your real ANTHROPIC_API_KEY

# Run the app
streamlit run app.py
```

---

## ✨ Features

- **5 Input Types** — User Story, Feature Description, Code Snippet, API Spec, Bug Report
- **5 Test Focuses** — All Types, Functional, Edge Cases, Negative, Security
- **Priority Filtering** — View High / Medium / Low priority cases separately
- **Tabbed Output** — All Cases, High Priority, Edge & Negative
- **Export** — Download as Markdown (.md) or CSV (.csv)
- **Gap Detection** — AI flags missing requirements or ambiguities
- **4 Built-in Examples** — Login, REST API, Search, Payment Flow

---

## 📁 Project Structure

```
sagarqa/
├── app.py                          # Main Streamlit app
├── requirements.txt                # Python dependencies
├── .gitignore                      # Excludes secrets
├── .streamlit/
│   ├── config.toml                 # Theme config
│   └── secrets.toml.example        # API key template (copy → secrets.toml)
└── README.md
```

---

## 💰 Monetisation (Next Steps)

Once live, add payments:
1. **Razorpay** — Indian payment gateway, easy integration
2. **Free tier** — 5 generations/day (track in session or DB)
3. **Pro tier** — ₹799/month unlimited
4. Add user auth with `streamlit-authenticator` or move to Django/Flask

---

## 🌊 About Sagar AI

Sagar AI builds tools that solve real human problems — starting with QA.

Built by C.S. Sagar — 15 years in software testing, tired of writing test cases by hand.

**sagar.ai** · *AI That Runs Deep*
