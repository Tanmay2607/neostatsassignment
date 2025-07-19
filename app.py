# --- 1. Imports ---
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import re

# --- 2. Helper: Extract code from LLM ---
def extract_python_code(response_text):
    match = re.search(r"```(?:python)?(.*?)```", response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return response_text.strip()

# --- 3. Gemini LLM call ---
def call_llm_with_gemini(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    return response.text.strip() if response.text else "❌ No response received."

# --- 4. Schema + Normalization ---
def normalize_column_names(df):
    return df.rename(columns=lambda col: ''.join(e for e in col.strip().lower().replace(' ', '_') if e.isalnum() or e == '_'))

def normalize_string_values(df):
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].astype(str).str.lower().str.replace(",", "").str.strip()
    if 'total' in df.columns:
        df['total'] = pd.to_numeric(df['total'], errors='coerce')
    return df

def get_data_schema(df):
    return ", ".join([f"{col} ({df[col].dtype})" for col in df.columns])

def generate_llm_prompt(query, schema):
    return f"""
You are an expert data analyst. You are given a user query and the schema of a pandas DataFrame named 'df'.
Your task is to generate a Python script to answer the query.

**Data Schema:**
{schema}

**User Query:**
"{query}"

**Instructions:**
1. Generate only executable Python code that uses the 'df' DataFrame.
2. Do NOT include explanations or text outside the code block.
3. The code must calculate the answer and assign it to a variable named `result`. 
   - If the query involves listing rows, assign the filtered DataFrame to `result`.
   - If it involves a value (like sum or count), assign the scalar to `result`.
4. If the query requires a visualization (e.g., "bar chart", "histogram"), generate valid code to create the plot using matplotlib.
   Use `st.pyplot(plt.gcf())` instead of `plt.show()` to display the chart in Streamlit.
5. Assume 'df' is already loaded.
6. When filtering by a text column, always use `.str.lower().replace(",", "").str.strip()` — never use `.lower()` directly on a Series or DataFrame.
7. Always check `.empty` before accessing `.iloc[0]` to avoid index errors.
8. Never use `.empty` on a string or scalar. Use `.empty` only on DataFrames or Series.
9. Never load data from a file. Do not use `pd.read_csv`, `pd.read_excel`, or any other file operations. The DataFrame named `df` is already loaded. Use it directly.
""".strip()

def execute_generated_code(code, df):
    local_scope = {'df': df, 'pd': pd, 'plt': plt, 'st': st}
    try:
        exec(code, {}, local_scope)
        result = local_scope.get("result", None)

        # If result is a DataFrame
        if isinstance(result, pd.DataFrame):
            if result.shape[0] <= 50:
                return result
            else:
                st.dataframe(result.head(50))
                return f"✅ Output truncated: Showing first 50 of {result.shape[0]} rows."

        # If result is a Series
        if isinstance(result, pd.Series):
            if result.name is None:
                result.name = "value"
            result_df = result.to_frame().reset_index()
            if result_df.shape[0] <= 50:
                return result_df
            else:
                st.dataframe(result_df.head(50))
                return f"✅ Output truncated: Showing first 50 of {result_df.shape[0]} rows."

        # If result is a scalar (int, float, bool, string)
        if isinstance(result, (int, float, bool, str)):
            return str(result)

        return "✅ Code executed successfully. (No specific output returned.)"

    except Exception as e:
        st.error("❌ Error executing generated code.")
        st.exception(e)
        return f"❌ Error executing code: {e}"

# --- 5. Streamlit App ---
st.set_page_config(page_title="NeoAT Excel Assistant", layout="centered")
st.title("Tanmay's Excel Sheet Analyzer")

api_key = st.secrets["gemini_api_key"]
uploaded_file = st.file_uploader("📁 Upload your Excel file", type=["xlsx"])
query = st.text_input("❓ Ask a question about your data")

if uploaded_file and api_key and query:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        df = normalize_column_names(df)
        df = normalize_string_values(df)
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        schema = get_data_schema(df)
        prompt = generate_llm_prompt(query, schema)
        with st.spinner("🤖 Thinking..."):
            response = call_llm_with_gemini(prompt, api_key)
            code = extract_python_code(response)
            result = execute_generated_code(code, df)

        st.subheader("💡 Answer / Chart")
        if isinstance(result, (pd.Series, pd.DataFrame)):
            st.write(result)
        elif result is not None:
            st.write(result)

    except Exception as e:
        st.error(f"❌ Failed to process: {e}")
