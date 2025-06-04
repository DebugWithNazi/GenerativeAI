import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import json
from datetime import datetime

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Set page config
st.set_page_config(
    page_title="Code Optimizer Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply light/dark theme
def apply_custom_css():
    dark_theme = """<style> .stApp {background-color:#1E1E1E;color:#FFF;} ... </style>"""
    light_theme = """<style> .stApp {background-color:#FFF;color:#000;} ... </style>"""
    st.markdown(dark_theme if st.session_state.theme == 'dark' else light_theme, unsafe_allow_html=True)

# Optimization logic with system prompt
def optimize_code(code, language):
    system_message = {
        "role": "system",
        "content": (
            "You are a professional code optimizer. "
            "Only answer questions related to code optimization. "
            "If a question is irrelevant or not about code, respond politely that you're only here to help with code optimization."
        )
    }

    user_prompt = (
        f"""Analyze, optimize, and correct the following {language} code. 
        Provide the following in your response:
        1. Optimized code
        2. Explanation of improvements
        3. Any potential bugs fixed
        4. Performance improvements made

        Here's the code:
        {code}
        """
    )

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                system_message,
                {"role": "user", "content": user_prompt}
            ],
            model="llama3-70b-8192"
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Save to history
def save_to_history(code, language, result):
    st.session_state.history.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'language': language,
        'original_code': code,
        'optimization_result': result
    })

# Save history to JSON
def save_history_to_file():
    try:
        with open('optimization_history.json', 'w') as f:
            json.dump(st.session_state.history, f, indent=4)
        return True
    except Exception:
        return False

# Main App
def main():
    apply_custom_css()

    # Sidebar
    with st.sidebar:
        st.title("⚙️ Settings")
        theme = st.radio("Choose Theme", ["light", "dark"])
        if theme != st.session_state.theme:
            st.session_state.theme = theme
            st.rerun()

        if st.button("💾 Save History"):
            st.success("History saved!" if save_history_to_file() else "Failed to save.")

        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.success("History cleared!")

    # Main Area
    st.title("🚀 Code Optimizer Pro")
    col1, col2 = st.columns([2, 1])

    with col1:
        languages = ["Python", "JavaScript", "Java", "C++", "Ruby", "Go", "PHP", "C#", "Swift", "Rust"]
        selected_language = st.selectbox("📝 Select Programming Language", languages)
        st.subheader("💻 Enter Your Code")
        user_code = st.text_area("Code Editor", height=300)

        if st.button("✨ Optimize Code"):
            if user_code.strip():
                with st.spinner("🔄 Optimizing..."):
                    result = optimize_code(user_code, selected_language)
                    save_to_history(user_code, selected_language, result)
                    st.markdown("### 🎉 Optimization Results")
                    st.markdown(result)
            else:
                st.error("⚠️ Please enter code to optimize.")

    with col2:
        st.subheader("📋 Optimization History")
        if st.session_state.history:
            for idx, entry in enumerate(reversed(st.session_state.history)):
                with st.expander(f"#{len(st.session_state.history)-idx}: {entry['language']} - {entry['timestamp']}"):
                    st.code(entry['original_code'], language=entry['language'].lower())
                    st.markdown("**Optimization Result:**")
                    st.markdown(entry['optimization_result'])
        else:
            st.info("No history yet.")

if __name__ == "__main__":
    main()
