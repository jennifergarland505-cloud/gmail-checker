import streamlit as st
import smtplib
import re
import pandas as pd

# পেজ সেটআপ (ব্রাউজার ট্যাবের নাম ও আইকন)
st.set_page_config(
    page_title="Gmail Checker - Accounts Validator",
    page_icon="📧",
    layout="centered"
)

# জিমেইল ফরম্যাট ভ্যালিডেশনের জন্য Regex ফাংশন
def is_valid_email_format(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
    return re.match(pattern, email) is not None

# SMTP দিয়ে জিমেইল চেক করার ফাংশন
def check_gmail(email):
    if not is_valid_email_format(email):
        return "Invalid Format"

    smtp_server = "gmail-smtp-in.l.google.com"
    port = 25

    try:
        # জিমেইলের SMTP সার্ভারে কানেক্ট করা
        server = smtplib.SMTP(smtp_server, port, timeout=6)
        server.helo()
        server.mail("test_checker@gmail.com")
        code, message = server.rcpt(email)
        server.quit()

        if code == 250:
            return "Active"
        else:
            return "Does Not Exist"
    except Exception as e:
        return "Connection Error"

# --- ইন্টারফেস ডিজাইন শুরু ---
st.title("📧 Gmail Account Checker")
st.write("এটি একটি সম্পূর্ণ ফ্রি এবং নিরাপদ জিমেইল ভ্যালিডেটর। কোনো পাসওয়ার্ড ছাড়াই জিমেইল চেক করুন।")

# সাইডবার অপশন
st.sidebar.header("⚙️ কন্ট্রোল প্যানেল")
mode = st.sidebar.radio("চেক করার মোড নির্বাচন করুন:", ["সিঙ্গেল ইমেইল চেক", "বাল্ক (ফাইল আপলোড) চেক"])

# --- মোড ১: সিঙ্গেল ইমেইল চেক ---
if mode == "সিঙ্গেল ইমেইল চেক":
    st.subheader("🔍 একক জিমেইল পরীক্ষা")
    single_email = st.text_input("আপনার জিমেইল অ্যাড্রেসটি লিখুন:", placeholder="example@gmail.com")
    
    if st.button("পরীক্ষা করুন", use_container_width=True):
        if single_email.strip():
            with st.spinner("চেক করা হচ্ছে..."):
                status = check_gmail(single_email.strip())
            
            # ফলাফলের ওপর ভিত্তি করে অ্যালার্ট বা বক্স দেখানো
            if status == "Active":
                st.success(f"✅ **{single_email}** - এই জিমেইলটি সক্রিয় এবং বিদ্যমান!")
            elif status == "Does Not Exist":
                st.error(f"❌ **{single_email}** - এই জিমেইলটির কোনো অস্তিত্ব নেই!")
            elif status == "Invalid Format":
                st.warning(f"⚠️ **{single_email}** - ইমেইলটির ফরম্যাট সঠিক নয়! (অবশ্যই @gmail.com হতে হবে)")
            else:
                st.info(f"ℹ️ দুঃখিত, সংযোগের সমস্যার কারণে চেক করা যায়নি। পুনরায় চেষ্টা করুন।")
        else:
            st.warning("অনুগ্রহ করে একটি ইমেইল লিখুন!")

# --- মোড ২: বাল্ক (ফাইল আপলোড) চেক ---
elif mode == "বাল্ক (ফাইল আপলোড) চেক":
    st.subheader("📁 ফাইল থেকে বাল্ক জিমেইল পরীক্ষা")
    st.write("নিচে একটি `.txt` ফাইল আপলোড করুন যেখানে প্রতি লাইনে একটি করে ইমেইল রয়েছে।")
    
    uploaded_file = st.file_uploader("TXT ফাইল আপলোড করুন", type=["txt"])
    
    if uploaded_file is not None:
        # ফাইল রিড করা
        emails = [line.decode("utf-8").strip() for line in uploaded_file if line.strip()]
        
        if len(emails) > 0:
            st.info(f"মোট {len(emails)}টি ইমেইল পাওয়া গেছে।")
            
            if st.button("চেকিং শুরু করুন", use_container_width=True):
                # প্রগ্রেস বার সেটআপ
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                results = []
                active_list = []
                inactive_list = []
                
                # লুপ চালিয়ে প্রতিটি ইমেইল চেক করা
                for idx, email in enumerate(emails):
                    status = check_gmail(email)
                    results.append({"Email": email, "Status": status})
                    
                    if status == "Active":
                        active_list.append(email)
                    else:
                        inactive_list.append(email)
                    
                    # প্রগ্রেস আপডেট
                    progress = (idx + 1) / len(emails)
                    progress_bar.progress(progress)
                    status_text.text(f"চেক হচ্ছে: {idx+1}/{len(emails)}")
                
                # সম্পূর্ণ ফলাফল টেবিলে দেখানো
                df = pd.DataFrame(results)
                st.write("### ফলাফল তালিকা:")
                st.dataframe(df, use_container_width=True)
                
                # ড্যাশবোর্ড স্ট্যাটাস কার্ড
                col1, col2 = st.columns(2)
                col1.metric("সক্রিয় জিমেইল (Active)", len(active_list))
                col2.metric("নিষ্ক্রিয়/ভুল (Inactive/Invalid)", len(inactive_list))
                
                # ডাউনলোড অপশন (সক্রিয় ইমেইলগুলোর জন্য)
                if active_list:
                    active_text = "\n".join(active_list)
                    st.download_button(
                        label="📥 সক্রিয় জিমেইলগুলোর তালিকা ডাউনলোড করুন (.txt)",
                        data=active_text,
                        file_name="active_emails.txt",
                        mime="text/plain"
                    )
        else:
            st.error("ফাইলটি খালি! অনুগ্রহ করে ইমেইল সম্বলিত ফাইল আপলোড করুন।")

# ফুটার
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Powered by Streamlit & Python SMTP</p>", unsafe_allow_html=True)
