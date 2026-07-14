import streamlit as st
import smtplib
import re
import pandas as pd
import time

# পেজ সেটআপ - ফুল ওয়াইড স্ক্রিন ও ডার্ক/লাইট অ্যাডাপ্টিভ থিম
st.set_page_config(
    page_title="GmailCheck.com - AI Validator",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ইমেইল ফরম্যাট চেক করার ফাংশন
def is_valid_email_format(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
    return re.match(pattern, email) is not None

# সরাসরি গুগল SMTP সার্ভারে চেক করার মেথড
def check_gmail(email):
    if not is_valid_email_format(email):
        return "Invalid Format"
    
    smtp_server = "gmail-smtp-in.l.google.com"
    port = 25
    try:
        server = smtplib.SMTP(smtp_server, port, timeout=3)
        server.helo()
        server.mail("dashboard_checker@gmail.com")
        code, message = server.rcpt(email)
        server.quit()
        
        if code == 250:
            return "Active"
        elif code == 550:
            return "Does Not Exist"
        else:
            return "Abnormal"
    except Exception:
        return "Abnormal"

# --- সিএসএস (CSS) দিয়ে স্ক্রিনশটের মতো স্টাইল তৈরি ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-title { font-size: 32px; font-weight: bold; color: #1e293b; margin-bottom: 5px; }
    .sub-title { font-size: 14px; color: #64748b; margin-bottom: 20px; }
    .status-tab { text-align: center; padding: 10px; border: 1px solid #e2e8f0; background-color: #ffffff; border-radius: 4px; font-weight: bold; }
    .status-active { background-color: #1e293b; color: white; border: 1px solid #1e293b; }
    .result-box { min-height: 250px; border: 1px solid #cbd5e1; border-radius: 4px; padding: 10px; background-color: #ffffff; font-family: monospace; white-space: pre-wrap; max-height: 250px; overflow-y: auto; }
    </style>
""", unsafe_allow_html=True)

# --- বাম পাশের মেনুবার (Sidebar Navigation) ---
with st.sidebar:
    st.markdown("## 🌐 GmailCheck.com")
    st.markdown("---")
    menu = st.radio(
        "নেভিগেশন মেনু",
        ["🔍 জিমেইল অ্যাকাউন্ট চেকার", "📊 ডাটা স্প্লিট ও রিমিক্স", "🔄 ডুপ্লিকেট রিমুভার", "📞 কাস্টমার সাপোর্ট"],
        label_visibility="collapsed"
    )

# --- মূল ড্যাশবোর্ড সেকশন ---
if menu == "🔍 জিমেইল অ্যাকাউন্ট চেকার":
    st.markdown('<div class="main-title">谷歌账号检查器 Gmailcheck</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">নিরাপদ ও দ্রুততম উপায়ে জিমেইল ভ্যালিডেশন করুন। কোনো পাসওয়ার্ডের প্রয়োজন নেই।</div>', unsafe_allow_html=True)
    
    # স্ক্রিনশটের মতো দুই কলামের লেআউট (বাম পাশে ইনপুট, ডান পাশে লাইভ রেজাল্ট)
    col_input, col_result = st.columns([1, 1], gap="large")
    
    with col_input:
        st.markdown("**অ্যাকাউন্ট তালিকা (এখানে আপনার ইমেইলগুলো পেস্ট করুন):**")
        input_text = st.text_area(
            "input_area",
            placeholder="name1@gmail.com\nname2@gmail.com\nname3@gmail.com\n\n*প্রতি লাইনে একটি করে ইমেইল দিন।",
            height=300,
            label_visibility="collapsed"
        )
        
        st.markdown("**টাইপ মোড:**")
        type_mode = st.radio("Mode", ["ব্যক্তিগত অ্যাকাউন্ট মোড (Personal)", "ব্যবসায়িক/মিক্সড মোড (Corporate)"], label_visibility="collapsed")
        
        st.markdown("**রুট লাইন স্পিড:**")
        speed_line = st.radio("Lines", ["ফ্রি সার্ভার লাইন (Free Route)", "ভিআইপি প্রিমিয়াম লাইন ১", "ভিআইপি প্রিমিয়াম লাইন ২"], horizontal=True, label_visibility="collapsed")
        
        # কন্ট্রোল অপশনস
        col_cb1, col_cb2 = st.columns(2)
        dup_check = col_cb1.checkbox("ডুপ্লিকেট ইমেইল স্বয়ংক্রিয়ভাবে বাদ দিন", value=True)
        ignore_err = col_cb2.checkbox("ভুল ফরম্যাটের ইমেইল এড়িয়ে যান", value=False)
        
        # সেফটি ডিলে
        delay = st.slider("রিকোয়েস্ট ডিলে স্পিড (সেকেন্ড):", 0.0, 2.0, 0.3, step=0.1)
        
        start_btn = st.button("⚡ চেকিং শুরু করুন (Start Checking)", use_container_width=True, type="primary")

    # ডাটা প্রসেসিং এবং ডান পাশের রেজাল্ট আউটপুট
    with col_result:
        # প্রগ্রেস বার
        progress_bar = st.progress(0)
        
        # ৪টি স্ট্যাটাস বক্সের জন্য লেআউট (১ম স্ক্রিনশটের ট্যাবগুলোর মতো)
        tab1, tab2, tab3, tab4 = st.columns(4)
        
        # প্লেসহোল্ডার কন্টেইনার (লাইভ আপডেট দেখানোর জন্য)
        box1 = st.empty()
        box2 = st.empty()
        box3 = st.empty()
        box4 = st.empty()
        
        # প্রাথমিক খালি বক্স স্টেট
        box1.markdown('<div class="result-box"></div>', unsafe_allow_html=True)
        box2.markdown('<div class="result-box"></div>', unsafe_allow_html=True)
        box3.markdown('<div class="result-box"></div>', unsafe_allow_html=True)
        box4.markdown('<div class="result-box"></div>', unsafe_allow_html=True)

        if start_btn and input_text.strip():
            # টেক্সট এরিয়া থেকে ইমেইলগুলো লাইনে লাইনে ভাগ করা
            raw_emails = [line.strip() for line in input_text.split("\n") if line.strip()]
            
            if dup_check:
                emails_to_check = list(dict.fromkeys(raw_emails))
            else:
                emails_to_check = raw_emails
                
            total = len(emails_to_check)
            
            active_res = []
            abnormal_res = []
            not_exist_res = []
            remaining_res = list(emails_to_check)
            
            # লুপের মাধ্যমে লাইভ চেকিং ও স্ক্রিন আপডেট
            for idx, email in enumerate(emails_to_check):
                status = check_gmail(email)
                
                if email in remaining_res:
                    remaining_res.remove(email)
                    
                if status == "Active":
                    active_res.append(email)
                elif status == "Does Not Exist":
                    not_exist_res.append(email)
                else:
                    abnormal_res.append(email)
                    
                # প্রগ্রেস বার ক্যালকুলেশন
                progress_bar.progress((idx + 1) / total)
                
                # ট্যাবের কাউন্টার সংখ্যা লাইভ আপডেট
                tab1.markdown(f'<div class="status-tab status-active">সক্রিয় ({len(active_res)})</div>', unsafe_allow_html=True)
                tab2.markdown(f'<div class="status-tab">অস্বাভাবিক ({len(abnormal_res)})</div>', unsafe_allow_html=True)
                tab3.markdown(f'<div class="status-tab">বিদ্যমান নেই ({len(not_exist_res)})</div>', unsafe_allow_html=True)
                tab4.markdown(f'<div class="status-tab">বাকি আছে ({len(remaining_res)})</div>', unsafe_allow_html=True)
                
                # বক্সগুলোর ভেতরের ডাটা লাইভ রিফ্রেশ
                box1.markdown(f'<div class="result-box">{"<br>".join(active_res)}</div>', unsafe_allow_html=True)
                box2.markdown(f'<div class="result-box">{"<br>".join(abnormal_res)}</div>', unsafe_allow_html=True)
                box3.markdown(f'<div class="result-box">{"<br>".join(not_exist_res)}</div>', unsafe_allow_html=True)
                box4.markdown(f'<div class="result-box">{"<br>".join(remaining_res)}</div>', unsafe_allow_html=True)
                
                time.sleep(delay)
                
            st.success("🎉 চেকিং সম্পন্ন হয়েছে!")
            
            # স্ক্রিনশটের নিচের ৪টি ডাউনলোড বাটনের মতো লেআউট
            st.markdown("---")
            btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
            
            if active_res:
                btn_col1.download_button("🟢 কপি সক্রিয় লিস্ট", "\n".join(active_res), file_name="active.txt", use_container_width=True)
            if abnormal_res:
                btn_col2.download_button("🟡 কপি অস্বাভাবিক লিস্ট", "\n".join(abnormal_res), file_name="abnormal.txt", use_container_width=True)
            if not_exist_res:
                btn_col3.download_button("🔴 কপি অনুপস্থিত লিস্ট", "\n".join(not_exist_res), file_name="not_exist.txt", use_container_width=True)
            if remaining_res:
                btn_col4.download_button("🟠 কপি অবশিষ্ট লিস্ট", "\n".join(remaining_res), file_name="remaining.txt", use_container_width=True)

# --- অন্যান্য ডামি পেজ (স্ক্রিনশটের মেনু বজায় রাখার জন্য) ---
else:
    st.subheader(f"🛠️ {menu} মডিউল")
    st.info("এই ফিচারটি প্রিমিয়াম সংস্করণে প্রক্রিয়াধীন রয়েছে।")
