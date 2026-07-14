import streamlit as st
import smtplib
import re
import pandas as pd

# Page setup ar title config
st.set_page_config(
    page_title="Gmail Account Checker",
    page_icon="📧",
    layout="centered"
)

# Email format check korar regex function
def is_valid_email_format(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
    return re.match(pattern, email) is not None

# SMTP diye Gmail active kina check korar main core function
def check_gmail(email):
    if not is_valid_email_format(email):
        return "Invalid Format"

    smtp_server = "gmail-smtp-in.l.google.com"
    port = 25

    try:
        # Connecting to Google's SMTP server
        server = smtplib.SMTP(smtp_server, port, timeout=5)
        server.helo()
        server.mail("test_checker@gmail.com")
        code, message = server.rcpt(email)
        server.quit()

        if code == 250:
            return "Active"
        else:
            return "Does Not Exist"
    except Exception as e:
        return "Connection Timeout/Error"

# --- UI Design ---
st.title("📧 Gmail Account Checker")
st.markdown("### Streamlit Light active validation system")
st.write("Apnar Gmail account check korar jonno single email athoba bulk TXT file use korun.")

# Navigation Sidebar
st.sidebar.header("⚙️ Control Panel")
mode = st.sidebar.radio("Checker Mode Select Karun:", ["Single Email Check", "Bulk Email (File Upload)"])

# --- MODE 1: Single Email Check ---
if mode == "Single Email Check":
    st.subheader("🔍 Single Email Validator")
    email_input = st.text_input("Gmail address-ti ekhane likhun:", placeholder="example@gmail.com")
    
    if st.button("Check Email", use_container_width=True):
        if email_input.strip():
            with st.spinner("Checking... Please wait..."):
                status = check_gmail(email_input.strip())
            
            # Status anujayi visual alert block
            if status == "Active":
                st.success(f"✅ **{email_input}** - Ai Gmail-ti fully Active ar active ache!")
            elif status == "Does Not Exist":
                st.error(f"❌ **{email_input}** - Ai Gmail-ti active nai ba exists kore na!")
            elif status == "Invalid Format":
                st.warning(f"⚠️ **{email_input}** - Email formating thik nai! Gmail address obosshoi @gmail.com hote hobe.")
            else:
                st.info("ℹ️ Connection error! Google SMTP port blocks request sometimes. Retry koren.")
        else:
            st.warning("Please enter a valid Gmail address.")

# --- MODE 2: Bulk Check (File Upload) ---
elif mode == "Bulk Email (File Upload)":
    st.subheader("📁 Bulk Gmail Validation (.txt)")
    st.write("Ekhane apnar text file upload korun. Protiti line-e ekti kore email thaka lagbe.")
    
    uploaded_file = st.file_uploader("Upload TXT File", type=["txt"])
    
    if uploaded_file is not None:
        # Decoded bytes to text string formatting
        emails = [line.decode("utf-8").strip() for line in uploaded_file if line.strip()]
        
        if len(emails) > 0:
            st.info(f"Total {len(emails)} emails found in this file.")
            
            if st.button("Start Bulk Checking", use_container_width=True):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                results = []
                active_list = []
                inactive_list = []
                
                for idx, email in enumerate(emails):
                    status = check_gmail(email)
                    results.append({"Email": email, "Status": status})
                    
                    if status == "Active":
                        active_list.append(email)
                    else:
                        inactive_list.append(email)
                    
                    # Progress state updates
                    progress = (idx + 1) / len(emails)
                    progress_bar.progress(progress)
                    status_text.text(f"Processed: {idx+1}/{len(emails)}")
                
                # Table reporting output
                df = pd.DataFrame(results)
                st.write("### Validation Result Table:")
                st.dataframe(df, use_container_width=True)
                
                # Overview Cards
                col1, col2 = st.columns(2)
                col1.metric("Active Emails ✅", len(active_list))
                col2.metric("Inactive/Error ❌", len(inactive_list))
                
                # Active email download block
                if active_list:
                    active_txt = "\n".join(active_list)
                    st.download_button(
                        label="📥 Download Active Emails Only",
                        data=active_txt,
                        file_name="verified_active_emails.txt",
                        mime="text/plain"
                    )
        else:
            st.error("Uploaded file is empty. Please verify your data inside .txt file.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Powered by GitHub & Streamlit Community Cloud</p>", unsafe_allow_html=True)
