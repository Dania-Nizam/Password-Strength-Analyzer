import math
import streamlit as st
import re

# Page styling
st.set_page_config(page_title="🔐 SecurePass: Password Strength Analyzer", page_icon="🔑", layout="centered")

# Custom CSS for enhanced UI
st.markdown(
    """
    <style>
        body {background-color: #eef2f7;}
        .main {text-align: center;}

        /* Center content */
        .block-container {
            max-width: 600px;
            margin: auto;
            padding: 20px;
            border-radius: 15px;
            background: white;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
        }

        /* Password Input Styling */
        .stTextInput input {
            width: 100% !important;
            border: 2px solid #3498db;
            border-radius: 12px;
            padding: 12px;
            font-size: 18px;
            text-align: center;
            transition: 0.3s;
        }
        .stTextInput input:focus {
            border-color: #2c3e50;
            box-shadow: 0px 0px 10px rgba(44, 62, 80, 0.3);
        }

        /* Password Length & Entropy UI */
        .info-box {
            background: #f9fafc;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .entropy {
            color: #3498db;
        }
        .length {
            color: #2c3e50;
        }

        /* Expander UI */
        .stExpander div[role="button"] {
            background: #2c3e50 !important;
            color: white !important;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
            text-align: center;
        }

        /* Keep button styles the same */
        .stButton button {
            width: 60%;
            background: linear-gradient(to right, #3498db, #2c3e50) !important;
            color: white !important;
            font-size: 18px;
            border-radius: 12px;
            padding: 12px;
            font-weight: bold;
            box-shadow: 0px 5px 12px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s ease-in-out;
        }
        .stButton button:hover {
            background: linear-gradient(to right, #2c3e50, #3498db) !important;
            transform: scale(1.05);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Page title and description
st.title("✨🔐 SecurePass: Password Strength Analyzer 🔑✨")
st.write("🛡️ **Ensure your password is strong and secure!** Enter your password below to check its security level. 🔍")

def calculate_entropy(password):
    character_sets = [
        (r"[A-Z]", 26),
        (r"[a-z]", 26),
        (r"\d", 10),
        (r"[!@#$%^&*]", 8)
    ]
    
    pool_size = sum(size for pattern, size in character_sets if re.search(pattern, password))
    entropy = len(password) * math.log2(pool_size) if pool_size else 0
    return entropy

def save_password(password):
    if password:
        if "saved_passwords" not in st.session_state:
            st.session_state.saved_passwords = []
        st.session_state.saved_passwords.append(password)
        st.success("💾 Password saved successfully!")

def show_saved_passwords():
    if "saved_passwords" in st.session_state and st.session_state.saved_passwords:
        st.write("🔒 **Saved Passwords:**")
        for pwd in st.session_state.saved_passwords:
            st.code(pwd)
    else:
        st.info("ℹ️ No saved passwords found.")

def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1 
    else:
        feedback.append("❌ Password should be **at least 8 characters long**")
    
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("🔠 Password should include **both uppercase (A-Z) and lowercase (a-z)**")
    
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("🔢 Password should include **at least one number (0-9)**")
    
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("🔣 Include **at least one special character (!@#$%^&*)**")
    
    entropy = calculate_entropy(password)
    
    # Display password strength results
    strength_labels = ["Weak", "Moderate", "Good", "Strong"]
    strength_message = strength_labels[score]
    
    if score == 4:
        st.success(f"✅ **{strength_message} Password** - Your password is very secure! 🔒")
    elif score == 3:
        st.info(f"⚠️ **{strength_message} Password** - Consider improving security by adding more features. 🛡️")
    else:
        st.error(f"❗ **{strength_message} Password** - Follow the suggestions below to strengthen it. 🚨")

    # Improved UI for Password Length & Entropy Score
    st.markdown(
        f"""
        <div class="info-box">
            <span class="length">🔢 **Password Length:** {len(password)} characters</span><br>
            <span class="entropy">📊 **Entropy Score:** {entropy:.2f} bits</span>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Improved UI for Password Improvement Suggestions
    if feedback:
        with st.expander("💡 **Improve Your Password** 🔧"):
            st.markdown(
                "<ul style='font-size: 16px;'>"
                + "".join(f"<li>{item}</li>" for item in feedback)
                + "</ul>",
                unsafe_allow_html=True,
            )

password = st.text_input("🔑 Enter your password:", type="password", help="Ensure your password is strong and secure.")

if st.button("🔍 Check Strength"):
    if password:
        check_password_strength(password)
    else:
        st.warning("⚠️ Please enter a password first! 🚫")

if st.button("💾 Save Password"):
    if password:
        save_password(password)
    else:
        st.warning("⚠️ Please enter a password before saving! 🚫")

if st.button("📂 Show Saved Passwords"):
    show_saved_passwords()
