# 📊 Tanmay's Excel Sheet Analyzer

A Streamlit-based conversational assistant that lets users upload Excel spreadsheets, ask natural language questions, and get instant answers as text, tables, or visual charts — all powered by Google's Gemini API.

---

## 🚀 Features

- **Upload Excel files** (`.xlsx`)  
- **Natural language queries**, like “count countries with total > 100”  
- **Dynamic Python code generation**  GEMINI AI 
- **Visual slides**: bar charts, histograms, etc., can display in Streamlit  
- **Smart normalization**: case-insensitive and punctuation-agnostic matching  
- **Safe execution**: handles DataFrame, Series, scalar outputs 

---

## 🛠️ Installation

 1. Clone the repo:
   ```bash
   git clone https://github.com/Tanmay2607/neoat.git
   cd neoat
   ```
 2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## ⚙️ Setup
1. Sign up at GEMINI AI and obtain your API key.
2. Add the key to Streamlit secrets:
   In ~/.streamlit/secrets.toml (locally) or via the Streamlit Cloud UI:
   ```
   gemini_api_key = "YOUR_GEMINI_API_KEY"
## ▶️ Run the App
```bash
streamlit run app.py
```
