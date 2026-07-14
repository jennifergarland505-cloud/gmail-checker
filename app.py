import streamlit as st
import smtplib
import re
import pandas as pd
import time
import os
from PIL import Image

st.set_page_config(
    page_title="Shakibul Hasan's GmailCheck.com - Premium Google Account Checker",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

def is_valid_email_format(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
    return re.match(pattern, email) is not None

def check_gmail(email):
    if not is_valid_email_format(email):
        return "Not exists"
    
    smtp_server = "gmail-smtp-in.l.google.com"
    port = 25
    try:
        server = smtplib.SMTP(smtp_server, port, timeout=3)
        server.helo()
        server.mail("dashboard_checker@gmail.com")
        code, message = server.rcpt(email)
        server.quit()
        
        if code == 250:
            return "Good"
        elif code == 550:
            return "Not exists"
        else:
            return "Verified" 
    except Exception:
        return "Verified"

st.markdown("""
    <style>
    .stApp { background-color: #f3f4f6; }
    
    .header-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 20px;
        border-radius: 8px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    
    div[data-testid="stSidebar"] { background-color: #0f172a; }
    div[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
    div[data-testid="stSidebar"] .st-emotion-cache-16tx1j3 { background-color: #1e293b; color: white !important; }

    .sidebar-img-container {
        display: flex;
        justify-content: center;
        margin-bottom: 15px;
    }
    div[data-testid="stSidebar"] img {
        border-radius: 50%;
        border: 2px solid #3b82f6;
        object-fit: cover;
    }

    .tab-btn {
        text-align: center;
        padding: 14px;
        font-weight: bold;
        font-size: 15px;
        border-radius: 6px;
        color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .btn-good { background-color: #10b981; border: 2px solid #047857; }
    .btn-verified { background-color: #3b82f6; border: 2px solid #1d4ed8; }
    .btn-notexists { background-color: #ef4444; border: 2px solid #b91c1c; }
    .btn-remaining { background-color: #f59e0b; border: 2px solid #b45309; }

    .result-box {
        min-height: 280px;
        max-height: 280px;
        overflow-y: auto;
        border-radius: 6px;
        padding: 12px;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        white-space: pre-wrap;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
    }
    .box-good { background-color: #ecfdf5; color: #065f46; border: 2px solid #a7f3d0; }
    .box-verified { background-color: #eff6ff; color: #1e40af; border: 2px solid #bfdbfe; }
    .box-notexists { background-color: #fef2f2; color: #991b1b; border: 2px solid #fecaca; }
    .box-remaining { background-color: #fffbeb; color: #92400e; border: 2px solid #fde68a; }

    div.stButton > button {
        border-radius: 6px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='color: black !important; text-align: center; margin-bottom: 5px;'>⚡ Shakibul Hasan (CSE)</h2>", unsafe_allow_html=True)
    
    image_path = "profile.png"
    
    if os.path.exists(image_path):
        try:
            saved_image = Image.open(image_path)
            st.markdown('<div class="sidebar-img-container">', unsafe_allow_html=True)
            st.image(saved_image, width=100)
            st.markdown('</div>', unsafe_allow_html=True)
        except Exception:
            pass
            
    uploaded_file = st.file_uploader("Upload Profile Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image.save(image_path)
        st.rerun()
    
    st.markdown("---")
    menu = st.sidebar.radio(
        "Menu",
        ["🔍 Google Check", "📊 Data Split and Merge", "🗑️ Remove Duplicates", "📞 Customer Support"],
        label_visibility="collapsed"
    )

if menu == "🔍 Google Check":
    st.markdown("""
        <div class="header-container">
            <h1 style='margin:0; font-size:32px;'>📧 Google Account Checker & Validator</h1>
            <p style='margin:5px 0 0 0; opacity:0.9;'>Secure, Fast and Direct Server-Based Bulk Gmail Validation Engine</p>
        </div>
    """, unsafe_allow_html=True)

    if "input_emails" not in st.session_state:
        st.session_state.input_emails = ""
    if "good_list" not in st.session_state:
        st.session_state.good_list = []
    if "verified_list" not in st.session_state:
        st.session_state.verified_list = []
    if "not_exist_list" not in st.session_state:
        st.session_state.not_exist_list = []
    if "remaining_list" not in st.session_state:
        st.session_state.remaining_list = []
    if "remaining_count" not in st.session_state:
        st.session_state.remaining_count = 0

    col_left, col_right = st.columns([1.1, 1], gap="large")
    
    with col_left:
        st.markdown("<h4 style='color: #1e293b; margin-bottom: 5px;'>📥 Account List (Paste your emails here):</h4>", unsafe_allow_html=True)
        input_text = st.text_area(
            "Input Area",
            value=st.session_state.input_emails,
            placeholder="example1@gmail.com\nexample2@gmail.com\nexample3@gmail.com",
            height=260,
            label_visibility="collapsed"
        )
        st.session_state.input_emails = input_text
        
        parsed_initial_emails = [line.strip() for line in input_text.split("\n") if line.strip()]
        if not st.session_state.good_list and not st
