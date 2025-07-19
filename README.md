# 📊 NeoStats Excel Chat Assistant

A Streamlit-based conversational assistant that lets users upload Excel spreadsheets, ask natural language questions, and get instant answers as text, tables, or visual charts — all powered by Google's Gemini API.

---

## 🚀 Features

- 📁 Upload `.xlsx` Excel files (single sheet expected)
- 🧠 Gemini LLM-powered analysis (Google Generative AI)
- 🧾 Auto-infers data types and schema
- ❓ Ask free-form natural language queries
- 📊 Visualize insights using matplotlib (bar charts, line charts, histograms, etc.)
- 🗂 Handles mixed datatypes, missing values, and inconsistent formatting
- 🔒 No hardcoded column assumptions — works on any structured Excel

---

## 🔧 Setup Instructions

### 1. Clone the Repo, Install Dependencies & Add API Key

```bash
# Clone the repository
git clone https://github.com/Tanmay2607/neostatsassignment.git
cd neostatsassignment

# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key
echo 'gemini_api_key = "YOUR_GEMINI_API_KEY"' > .streamlit/secrets.toml
Get your key from GOOGLEAISTUDIO
