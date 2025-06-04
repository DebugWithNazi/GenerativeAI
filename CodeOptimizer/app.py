import streamlit as st
import os
from groq import Groq
import json
from datetime import datetime

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Set page configuration
st.set_page_config(
    page_title="Code Optimizer Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for light and dark themes
def apply_custom_css():
    dark_theme = """
    <style>
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .stTextArea textarea {
            background-color: #2D2D2D !important;
            color: #FFFFFF !important;
            border: 1px solid #3D3D3D !important;
        }
        .stTextArea textarea:focus {
            box-shadow: 0 0 0 2px #4D4D4D !important;
        }
        .stTextArea textarea::selection {
            background-color: #264F78 !important;
            color: #FFFFFF !important;
        }
        .stButton button {
            background-color: #0078D4 !important;
            color: white !important;
            border-radius: 5px !important;
            padding: 10px 20px !important;
            border: none !important;
        }
        .stButton button:hover {
            background-color: #2B88D8 !important;
        }
        .stSelectbox > div > div {
            background-color: #2D2D2D !important;
            color: #FFFFFF !important;
        }
        .stSelectbox > div > div > div {
            color: #FFFFFF !important;
        }
        .stSelectbox > div > div[aria-expanded=true] > div:last-child {
            background-color: #2D2D2D !important;
            color: #FFFFFF !important;
        }
        .sidebar .sidebar-content {
            background-color: #252526 !important;
        }
        .streamlit-expanderHeader {
            background-color: #2D2D2D !important;
            color: #FFFFFF !important;
        }
        .streamlit-expanderContent {
            background-color: #1E1E1E !important;
            color: #FFFFFF !important;
        }
        .stMarkdown code {
            background-color: #2D2D2D !important;
            color: #FFFFFF !important;
        }
        .stSuccess, .stInfo {
            background-color: #2D2D2D !important;
            color: #FFFFFF !important;
        }
        .stError {
            background-color: #442726 !important;
            color: #FFFFFF !important;
        }
    </style>
    """
    
    light_theme = """
    <style>
        .stApp {
            background-color: #FFFFFF;
            color: #000000;
        }
        .stTextArea textarea {
            background-color: #F0F2F6 !important;
            color: #000000 !important;
            border: 1px solid #E0E0E0 !important;
        }
        .stTextArea textarea:focus {
            box-shadow: 0 0 0 2px #0078D4 !important;
        }
        .stButton button {
            background-color: #0078D4 !important;
            color: white !important;
            border-radius: 5px !important;
            padding: 10px 20px !important;
            border: none !important;
        }
        .stButton button:hover {
            background-color: #2B88D8 !important;
        }
        .stSelectbox > div > div {
            background-color: #FFFFFF !important;
        }
        .stSuccess, .stInfo {
            background-color: #E8F0FE !important;
            color: #000000 !important;
        }
        .stError {
            background-color: #FDE7E9 !important;
            color: #000000 !important;
        }
    </style>
    """
    
    if st.session_state.theme == 'dark':
        st.markdown(dark_theme, unsafe_allow_html=True)
    else:
        st.markdown(light_theme, unsafe_allow_html=True)

# Initialize Groq client
client = Groq(api_key="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")

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

# Save result to history
def save_to_history(code, language, result):
    st.session_state.history.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'language': language,
        'original_code': code,
        'optimization_result': result
    })

# Save history to JSON file
def save_history_to_file():
    try:
        with open('optimization_history.json', 'w') as f:
            json.dump(st.session_state.history, f, indent=4)
        return True
    except Exception as e:
        return False

# Main app logic
def main():
    apply_custom_css()

    # Sidebar
    with st.sidebar:
        st.title("⚙️ Settings")
        theme = st.radio(
            "Choose Theme",
            ["light", "dark"],
            index=0 if st.session_state.theme == 'light' else 1
        )
        if theme != st.session_state.theme:
            st.session_state.theme = theme
            st.rerun()

        if st.button("💾 Save History", key="save_history"):
            if save_history_to_file():
                st.success("History saved successfully!")
            else:
                st.error("Failed to save history")

        if st.button("🗑️ Clear History", key="clear_history"):
            st.session_state.history = []
            st.success("History cleared!")

    # Main content
    st.title("🚀 Code Optimizer Pro")
    col1, col2 = st.columns([2, 1])

    with col1:
        languages = ["Python", "JavaScript", "Java", "C++", "Ruby", "Go", "PHP", "C#", "Swift", "Rust"]
        selected_language = st.selectbox("📝 Select Programming Language", languages, key="lang_select")
        st.subheader("💻 Enter Your Code")
        user_code = st.text_area("Code Editor", height=300, key="code_input")

        if st.button("✨ Optimize Code", key="optimize"):
            if user_code.strip():
                with st.spinner("🔄 Magic in progress..."):
                    result = optimize_code(user_code, selected_language)
                    save_to_history(user_code, selected_language, result)
                    st.markdown("### 🎉 Optimization Results")
                    st.markdown(result)
            else:
                st.error("⚠️ Please enter some code to optimize")

    with col2:
        st.subheader("📋 Optimization History")
        if st.session_state.history:
            for idx, entry in enumerate(reversed(st.session_state.history)):
                with st.expander(f"#{len(st.session_state.history)-idx}: {entry['language']} - {entry['timestamp']}"):
                    st.code(entry['original_code'], language=entry['language'].lower())
                    st.markdown("**Optimization Result:**")
                    st.markdown(entry['optimization_result'])
        else:
            st.info("No optimization history yet")

if __name__ == "__main__":
    main()
