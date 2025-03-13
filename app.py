import re
import streamlit as st
import random
import string

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if any(char.isupper() for char in password) and any(char.islower() for char in password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if any(char in "!@#$%^&*()" for char in password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    return score, feedback

def generate_password(length=10, use_digits=True, use_special=True):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special:
        characters += "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(length))

st.set_page_config(page_icon="🔐", page_title="Password Tool", layout="wide")

# Theme Initialization in session state
if "theme" not in st.session_state:
    st.session_state.theme = "blue"

# Sidebar Navigation
st.sidebar.title("🔐 Secure Password Tool")

# ✅ Correct Toggle Implementation
if st.sidebar.button("🌗 Blue/Green Mode"):
    st.session_state.theme = "green" if st.session_state.theme == "blue" else "blue"

# Apply Theme Based CSS
themes = {
    "blue": {"primary_bg": "#00334E", "sidebar_bg": "#145374", "text_color": "#E8E8E8", "text_color1": "#080808"},
    "green": {"primary_bg": "#2F4F2F", "sidebar_bg": "#3E6D3E", "text_color": "#E8E8E8", "text_color1": "#080808"},
}

theme_colors = themes[st.session_state.theme]

st.markdown(
    f"""
    <style>
        html, body, [class*="stApp"] {{
            background-color: {theme_colors["primary_bg"]} !important;
        }}
        div[data-testid="stMarkdownContainer"] {{
            color: {theme_colors["text_color"]} !important;
        }}
        div[data-testid="stCode"] pre {{
            background-color: {theme_colors["text_color"]} !important;
            color: {theme_colors["text_color1"]};
        }}
        section[data-testid="stSidebar"] {{
            background-color: {theme_colors["sidebar_bg"]} !important;
        }}
        div[data-testid="stSliderTickBarMin"] {{
            color: {theme_colors["text_color"]} !important;
        }}
        div[data-testid="stSliderTickBarMax"] {{
            color: {theme_colors["text_color"]} !important;
        }}
        .main-title {{
            text-align: center;
        }}
        input {{
            background-color: {theme_colors["sidebar_bg"]} !important;
            color: {theme_colors["text_color"]} !important;
        }}
        div[data-baseweb="input"] > div {{
            border: none !important;
            box-shadow: none !important;
        }}
        div[data-testid="stTextInputRootElement"] {{
            background-color: {theme_colors["sidebar_bg"]} !important;
            padding: 5px;
        }}
        button {{
            background-color: {theme_colors["sidebar_bg"]} !important;
            color: {theme_colors["text_color"]} !important;
        }}
        .footer {{
            position: fixed;
            left: 50%;
            bottom: 0;
            transform: translateX(-50%);
            text-align: center;
            padding: 12px;
            font-size: 14px;
            font-weight: bold;
            background: {theme_colors["sidebar_bg"]};
            border-top: 3px solid {theme_colors["text_color"]};
            width: 100%;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Session state for password history
if 'password_history' not in st.session_state:
    st.session_state['password_history'] = []

# Sidebar Navigation
page = st.sidebar.radio("Select a Page:", ["Password Strength Meter", "Password Generator"])

# Password Strength Meter
if page == "Password Strength Meter":
    st.markdown("<h1 class='main-title'>🔒 Password Strength Meter</h1>", unsafe_allow_html=True)
    st.markdown("---")

    def trigger_check_strength():
        st.session_state["enter_pressed"] = True

    password = st.text_input("Enter your password:", type="password", on_change=trigger_check_strength)

    if st.button("Check Strength") or (password and st.session_state.get("enter_pressed", False)):
        st.session_state["enter_pressed"] = False  # Reset after pressing Enter

        if password:
            strength, feedback = check_password_strength(password)

            # Custom progress bar with multiple colors
            progress_html = f"""
            <div style="width: 100%; height: 10px; display: flex; border-radius: 5px; overflow: hidden;">
                <div style="width: 25%; background-color: {'red' if strength >= 1 else '#E8E8E8'};"></div>
                <div style="width: 25%; background-color: {'orange' if strength >= 2 else '#E8E8E8'};"></div>
                <div style="width: 25%; background-color: {'yellow' if strength >= 3 else '#E8E8E8'};"></div>
                <div style="width: 25%; background-color: {'green' if strength >= 4 else '#E8E8E8'};"></div>
            </div>
            """
            st.markdown(progress_html, unsafe_allow_html=True)

            if strength == 4:
                st.success("✅ Strong Password!")
                st.balloons()
            elif strength == 3:
                st.warning("⚠️ Moderate Password - Consider adding more security features.")
            else:
                st.error("❌ Weak Password - Improve it using the suggestions below.")

            if feedback:
                st.write("### Suggestions:")
                for tip in feedback:
                    st.write(f"- {tip}")
        else:
            st.warning("Please enter a password to check its strength.")

    st.markdown(
        """
        <script>
        document.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                event.preventDefault();
                window.parent.document.querySelector('button[kind="primary"]').click();
            }
        });
        </script>
        """,
        unsafe_allow_html=True,
    )
# Password Generator
elif page == "Password Generator":
    st.markdown("<h1 class='main-title'>🔑 Password Generator</h1>", unsafe_allow_html=True)
    st.markdown("---")
    length = st.slider("Select password length:", 8, 16, 10)
    use_digits = st.checkbox("Include Numbers", True)
    use_special = st.checkbox("Include Special Characters", True)
    
    if st.button("Generate Password"):
        password = generate_password(length, use_digits, use_special)
        st.write("**Generated Password:**")
        st.code(password)
        if password not in st.session_state["password_history"]:
            st.session_state["password_history"].append(password)
    
    if st.session_state['password_history']:
        st.write("### Password History")
        for p in st.session_state['password_history']:
            st.code(p)
        st.markdown("</div>", unsafe_allow_html=True)
        
    if st.button("Clear History"):
        st.session_state['password_history'] = []
        st.rerun()

st.markdown("<div class='footer'>Made by Muhammad Ahmed 🔐</div>", unsafe_allow_html=True)
