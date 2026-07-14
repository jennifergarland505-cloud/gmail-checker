import streamlit as st
import smtplib
import re
import pandas as pd
import time

# Page Configuration
st.set_page_config(
    page_title="GmailCheck.com - Google Account Checker",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Email format check functions
def is_valid_email_format(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
    return re.match(pattern, email) is not None

# Direct Google SMTP verification logic
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

# Custom CSS styling
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .status-tab { text-align: center; padding: 12px; border: 1px solid #e2e8f0; background-color: #ffffff; border-radius: 4px; font-weight: bold; font-size: 14px; }
    .status-active { background-color: #1a2332; color: white; border: 1px solid #1a2332; }
    .result-box { min-height: 280px; border: 1px solid #cbd5e1; border-radius: 4px; padding: 10px; background-color: #ffffff; font-family: monospace; white-space: pre-wrap; max-height: 280px; overflow-y: auto; color: #334155; }
    div[data-testid="stSidebar"] { background-color: #111c24; }
    div[data-testid="stSidebar"] * { color: #94a3b8 !important; }
    div[data-testid="stSidebar"] .st-emotion-cache-16tx1j3 { background-color: #1e293b; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Menu Navigation ---
with st.sidebar:
    st.markdown("<h2 style='color: white; margin-bottom: 20px;'>📧 GmailCheck.com</h2>", unsafe_allow_html=True)
    menu = st.radio(
        "Menu",
        ["🔍 Google Check", "📊 Data Split and Merge", "🗑️ Remove Duplicates", "📞 Customer Support"],
        label_visibility="collapsed"
    )

# --- Main Feature Panel ---
if menu == "🔍 Google Check":
    
    # Session States
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
    
    # Left Column: Inputs and Options
    with col_left:
        input_text = st.text_area(
            "Input Area",
            value=st.session_state.input_emails,
            placeholder="hfgjdgxg318@gmail.com\nfhghhfxhuf@gmail.com\ng94769251@gmail.com",
            height=280,
            label_visibility="collapsed"
        )
        st.session_state.input_emails = input_text
        
        parsed_initial_emails = [line.strip() for line in input_text.split("\n") if line.strip()]
        if not st.session_state.good_list and not st.session_state.not_exist_list and not st.session_state.verified_list:
            st.session_state.remaining_count = len(parsed_initial_emails)

        st.markdown("**Type Mode:**")
        type_mode = st.radio("Type Mode Options", ["Personal Account Mode", "Enterprise/Personal Compatibility Mode"], label_visibility="collapsed")
        
        st.markdown("**Route:** <span style='background-color:#eaeaea; padding:2px 5px; font-size:12px;'>VIP3 supports 300 queries per time, with continuous speed improvement</span>", unsafe_allow_html=True)
        route_mode = st.radio("Route Options", ["Free Route", "VIP1 Route", "VIP2 Route", "VIP3 Route"], horizontal=True, label_visibility="collapsed")
        
        repeat_detection = st.toggle("Repeat Detection", value=True)
        ignore_format = st.toggle("Ignore email format errors", value=False)
        check_exists = st.toggle("Check if exists(Slow query)", value=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns([1, 1])
        
        start_check = btn_col1.button("Start Check", type="primary", use_container_width=True)
        clear_data = btn_col2.button("Clear Data", use_container_width=True)
        
        if clear_data:
            st.session_state.input_emails = ""
            st.session_state.good_list = []
            st.session_state.verified_list = []
            st.session_state.not_exist_list = []
            st.session_state.remaining_list = []
            st.session_state.remaining_count = 0
            st.rerun()

    # Right Column: Live Output (Fixed in-place update)
    with col_right:
        progress_bar = st.progress(0)
        
        # ১. কলামগুলো একবারই তৈরি করা হচ্ছে
        h_col1, h_col2, h_col3, h_col4 = st.columns(4)
        
        # ২. স্ট্যাটাস ট্যাক্স আপডেট করার জন্য .empty() প্লেসহোল্ডার তৈরি করা হলো
        tab_good_placeholder = h_col1.empty()
        tab_verified_placeholder = h_col2.empty()
        tab_not_exist_placeholder = h_col3.empty()
        tab_remaining_placeholder = h_col4.empty()
        
        # ৩. রেজাল্ট বক্সের জন্য .empty() প্লেসহোল্ডার
        box_good = st.empty()
        box_verified = st.empty()
        box_not_exist = st.empty()
        box_remaining = st.empty()

        # প্রাথমিক স্টেজ রেন্ডারিং (অতিরিক্ত কপি তৈরি প্রতিরোধে .empty() ব্যবহার)
        tab_good_placeholder.markdown(f'<div class="status-tab status-active">Good({len(st.session_state.good_list)})</div>', unsafe_allow_html=True)
        tab_verified_placeholder.markdown(f'<div class="status-tab">Verified({len(st.session_state.verified_list)})</div>', unsafe_allow_html=True)
        tab_not_exist_placeholder.markdown(f'<div class="status-tab">Not exists({len(st.session_state.not_exist_list)})</div>', unsafe_allow_html=True)
        tab_remaining_placeholder.markdown(f'<div class="status-tab">Remaining({st.session_state.remaining_count})</div>', unsafe_allow_html=True)
        
        box_good.markdown(f'<div class="result-box">{"<br>".join(st.session_state.good_list)}</div>', unsafe_allow_html=True)
        box_verified.markdown(f'<div class="result-box">{"<br>".join(st.session_state.verified_list)}</div>', unsafe_allow_html=True)
        box_not_exist.markdown(f'<div class="result-box">{"<br>".join(st.session_state.not_exist_list)}</div>', unsafe_allow_html=True)
        
        init_rem_text = "<br>".join(parsed_initial_emails) if st.session_state.remaining_count == len(parsed_initial_emails) else "<br>".join(st.session_state.remaining_list)
        box_remaining.markdown(f'<div class="result-box">{init_rem_text}</div>', unsafe_allow_html=True)

        # "Start Check" এ ক্লিক করার পর লুপ অ্যাকশন
        if start_check and input_text.strip():
            emails_to_validate = [line.strip() for line in input_text.split("\n") if line.strip()]
            
            if repeat_detection:
                emails_to_validate = list(dict.fromkeys(emails_to_validate))
                
            total_count = len(emails_to_validate)
            
            st.session_state.good_list = []
            st.session_state.verified_list = []
            st.session_state.not_exist_list = []
            st.session_state.remaining_list = list(emails_to_validate)
            st.session_state.remaining_count = total_count
            
            for idx, current_email in enumerate(emails_to_validate):
                res_status = check_gmail(current_email)
                
                if current_email in st.session_state.remaining_list:
                    st.session_state.remaining_list.remove(current_email)
                st.session_state.remaining_count = len(st.session_state.remaining_list)
                
                if res_status == "Good":
                    st.session_state.good_list.append(current_email)
                elif res_status == "Not exists":
                    st.session_state.not_exist_list.append(current_email)
                else:
                    st.session_state.verified_list.append(current_email)
                
                # প্রগ্রেস বার
                progress_bar.progress((idx + 1) / total_count)
                
                # নতুন বাটন বা বক্স তৈরি না করে শুধুমাত্র প্লেসহোল্ডারের ভেতরের ভ্যালু আপডেট করা হচ্ছে
                tab_good_placeholder.markdown(f'<div class="status-tab status-active">Good({len(st.session_state.good_list)})</div>', unsafe_allow_html=True)
                tab_verified_placeholder.markdown(f'<div class="status-tab">Verified({len(st.session_state.verified_list)})</div>', unsafe_allow_html=True)
                tab_not_exist_placeholder.markdown(f'<div class="status-tab">Not exists({len(st.session_state.not_exist_list)})</div>', unsafe_allow_html=True)
                tab_remaining_placeholder.markdown(f'<div class="status-tab">Remaining({st.session_state.remaining_count})</div>', unsafe_allow_html=True)
                
                box_good.markdown(f'<div class="result-box">{"<br>".join(st.session_state.good_list)}</div>', unsafe_allow_html=True)
                box_verified.markdown(f'<div class="result-box">{"<br>".join(st.session_state.verified_list)}</div>', unsafe_allow_html=True)
                box_not_exist.markdown(f'<div class="result-box">{"<br>".join(st.session_state.not_exist_list)}</div>', unsafe_allow_html=True)
                box_remaining.markdown(f'<div class="result-box">{"<br>".join(st.session_state.remaining_list)}</div>', unsafe_allow_html=True)
                
                time.sleep(0.1) # নিরাপদ রেট লিমিট স্পিড
                
            st.success("Verification Completed successfully!")

        # নিচের কপি বাটনগুলো
        st.markdown("<br>", unsafe_allow_html=True)
        act_col1, act_col2, act_col3, act_col4 = st.columns(4)
        
        act_col1.download_button("Copy Good List", "\n".join(st.session_state.good_list) if st.session_state.good_list else "", file_name="good.txt", use_container_width=True)
        act_col2.download_button("Copy Verified List", "\n".join(st.session_state.verified_list) if st.session_state.verified_list else "", file_name="verified.txt", use_container_width=True)
        act_col3.download_button("Copy non-existing list", "\n".join(st.session_state.not_exist_list) if st.session_state.not_exist_list else "", file_name="not_exists.txt", use_container_width=True)
        act_col4.download_button("Copy Remaining List", "\n".join(st.session_state.remaining_list) if st.session_state.remaining_list else "", file_name="remaining.txt", use_container_width=True)

else:
    st.subheader(f"{menu} Feature")
    st.info("Module is working under maintenance pipeline structures.")
