import streamlit as st
import smtplib
import re
import pandas as pd
import time

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
    st.markdown("<h2 style='color: black !important; text-align: center;'>⚡ Shakibul Hasan (CSE)</h2>", unsafe_allow_html=True)
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
        if not st.session_state.good_list and not st.session_state.not_exist_list and not st.session_state.verified_list:
            st.session_state.remaining_count = len(parsed_initial_emails)

        st.markdown("**Type Mode:**")
        type_mode = st.radio("Type Mode Options", ["Personal Account Mode", "Enterprise/Personal Compatibility Mode"], label_visibility="collapsed")
        
        st.markdown("**Route:** <span style='background-color:#ffe4e6; color:#9f1239; padding:2px 8px; font-size:12px; border-radius:4px; font-weight:bold;'>VIP3 supports 300 queries per session, with optimized speed performance</span>", unsafe_allow_html=True)
        route_mode = st.radio("Route Options", ["Free Route", "VIP1 Route", "VIP2 Route", "VIP3 Route"], horizontal=True, label_visibility="collapsed")
        
        col_sw1, col_sw2, col_sw3 = st.columns(3)
        with col_sw1:
            repeat_detection = st.toggle("Repeat Detection", value=True)
        with col_sw2:
            ignore_format = st.toggle("Ignore email errors", value=False)
        with col_sw3:
            check_exists = st.toggle("Check Exists (Slow)", value=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns([1.2, 1])
        
        start_check = btn_col1.button("🚀 Start Checker Line", type="primary", use_container_width=True)
        clear_data = btn_col2.button("🗑️ Clear Live Data", use_container_width=True)
        
        if clear_data:
            st.session_state.input_emails = ""
            st.session_state.good_list = []
            st.session_state.verified_list = []
            st.session_state.not_exist_list = []
            st.session_state.remaining_list = []
            st.session_state.remaining_count = 0
            st.rerun()

    with col_right:
        progress_bar = st.progress(0)
        
        h_col1, h_col2, h_col3, h_col4 = st.columns(4)
        
        tab_good_placeholder = h_col1.empty()
        tab_verified_placeholder = h_col2.empty()
        tab_not_exist_placeholder = h_col3.empty()
        tab_remaining_placeholder = h_col4.empty()
        
        box_good = st.empty()
        box_verified = st.empty()
        box_not_exist = st.empty()
        box_remaining = st.empty()

        tab_good_placeholder.markdown(f'<div class="tab-btn btn-good">Good ({len(st.session_state.good_list)})</div>', unsafe_allow_html=True)
        tab_verified_placeholder.markdown(f'<div class="tab-btn btn-verified">Verified ({len(st.session_state.verified_list)})</div>', unsafe_allow_html=True)
        tab_not_exist_placeholder.markdown(f'<div class="tab-btn btn-notexists">Not exist ({len(st.session_state.not_exist_list)})</div>', unsafe_allow_html=True)
        tab_remaining_placeholder.markdown(f'<div class="tab-btn btn-remaining">Remaining ({st.session_state.remaining_count})</div>', unsafe_allow_html=True)
        
        box_good.markdown(f'<div class="result-box box-good">{"<br>".join(st.session_state.good_list)}</div>', unsafe_allow_html=True)
        box_verified.markdown(f'<div class="result-box box-verified">{"<br>".join(st.session_state.verified_list)}</div>', unsafe_allow_html=True)
        box_not_exist.markdown(f'<div class="result-box box-notexists">{"<br>".join(st.session_state.not_exist_list)}</div>', unsafe_allow_html=True)
        
        init_rem_text = "<br>".join(parsed_initial_emails) if st.session_state.remaining_count == len(parsed_initial_emails) else "<br>".join(st.session_state.remaining_list)
        box_remaining.markdown(f'<div class="result-box box-remaining">{init_rem_text}</div>', unsafe_allow_html=True)

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
                
                progress_bar.progress((idx + 1) / total_count)
                
                tab_good_placeholder.markdown(f'<div class="tab-btn btn-good">Good ({len(st.session_state.good_list)})</div>', unsafe_allow_html=True)
                tab_verified_placeholder.markdown(f'<div class="tab-btn btn-verified">Verified ({len(st.session_state.verified_list)})</div>', unsafe_allow_html=True)
                tab_not_exist_placeholder.markdown(f'<div class="tab-btn btn-notexists">Not exist ({len(st.session_state.not_exist_list)})</div>', unsafe_allow_html=True)
                tab_remaining_placeholder.markdown(f'<div class="tab-btn btn-remaining">Remaining ({st.session_state.remaining_count})</div>', unsafe_allow_html=True)
                
                box_good.markdown(f'<div class="result-box box-good">{"<br>".join(st.session_state.good_list)}</div>', unsafe_allow_html=True)
                box_verified.markdown(f'<div class="result-box box-verified">{"<br>".join(st.session_state.verified_list)}</div>', unsafe_allow_html=True)
                box_not_exist.markdown(f'<div class="result-box box-notexists">{"<br>".join(st.session_state.not_exist_list)}</div>', unsafe_allow_html=True)
                box_remaining.markdown(f'<div class="result-box box-remaining">{"<br>".join(st.session_state.remaining_list)}</div>', unsafe_allow_html=True)
                
                time.sleep(0.1)
                
            st.success("Verification Completed successfully!")

        st.markdown("<br>", unsafe_allow_html=True)
        act_col1, act_col2, act_col3, act_col4 = st.columns(4)
        
        act_col1.download_button("🟢 Copy Good List", "\n".join(st.session_state.good_list) if st.session_state.good_list else "", file_name="good.txt", use_container_width=True)
        act_col2.download_button("🔵 Copy Verified List", "\n".join(st.session_state.verified_list) if st.session_state.verified_list else "", file_name="verified.txt", use_container_width=True)
        act_col3.download_button("🔴 Copy non-existing list", "\n".join(st.session_state.not_exist_list) if st.session_state.not_exist_list else "", file_name="not_exists.txt", use_container_width=True)
        act_col4.download_button("🟡 Copy Remaining List", "\n".join(st.session_state.remaining_list) if st.session_state.remaining_list else "", file_name="remaining.txt", use_container_width=True)

else:
    st.subheader(f"{menu} Feature")
    st.info("Module is working under maintenance pipeline structures.")
