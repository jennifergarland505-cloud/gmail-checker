import streamlit as st
import smtplib
import re
import pandas as pd
import time

# পেজ কনফিগারেশন
st.set_page_config(
    page_title="Premium Gmail Validator Pro",
    page_icon="🛡️",
    layout="wide"
)

# ইমেইল ফরম্যাট চেক করার ফাংশন
def is_valid_email_format(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
    return re.match(pattern, email) is not None

# জিমেইল সার্ভার ভ্যালিডেশন ফাংশন
def check_gmail(email):
    if not is_valid_email_format(email):
        return "Invalid Format"

    smtp_server = "gmail-smtp-in.l.google.com"
    port = 25

    try:
        server = smtplib.SMTP(smtp_server, port, timeout=4)
        server.helo()
        server.mail("premium_checker@gmail.com")
        code, message = server.rcpt(email)
        server.quit()

        if code == 250:
            return "Active/Exist"
        elif code == 550:
            return "Does Not Exist"
        else:
            return "Blocked/Protected"
    except Exception:
        return "Connection Timeout"

# --- প্রিমিয়াম ইন্টারফেস ---
st.title("🛡️ Premium Gmail Account Validator Pro")
st.write("এটি একটি অ্যাডভান্সড বাল্ক ইমেইল চেকিং সিস্টেম যা গুগলের SMTP সার্ভারের সাথে সরাসরি যোগাযোগ করে অ্যাকাউন্ট ভ্যালিডেশন করে।")

# সাইডবার কন্ট্রোল প্যানেল
st.sidebar.header("⚙️ Settings Panel")
mode = st.sidebar.radio("সিলেক্ট করুন:", ["Bulk Email (File Upload)", "Single Email Check"])

# স্প্যাম বা আইপি ব্লক এড়ানোর জন্য ডিলে টাইম (Premium Feature)
delay_time = st.sidebar.slider("Delay between requests (Seconds):", 0.1, 3.0, 0.5, step=0.1)
st.sidebar.caption("💡 টিপস: ১ সেকেন্ড বা তার বেশি ডিলে রাখলে গুগলের আইপি ব্লক করার রিস্ক থাকে না।")

# --- মোড ১: বাল্ক চেকিং (Default Main Feature) ---
if mode == "Bulk Email (File Upload)":
    st.subheader("📁 বাল্ক জিমেইল পরীক্ষা ও ফিল্টারিং")
    
    uploaded_file = st.file_uploader("আপনার .txt ফাইলটি এখানে আপলোড করুন", type=["txt"])
    
    if uploaded_file is not None:
        # ফাইল থেকে ইমেইল রিড করা এবং ফাকা লাইন বাদ দেওয়া
        raw_emails = [line.decode("utf-8").strip() for line in uploaded_file if line.strip()]
        
        # ডুপ্লিকেট ইমেইল রিমুভ করা (Premium Feature)
        unique_emails = list(dict.fromkeys(raw_emails))
        duplicate_count = len(raw_emails) - len(unique_emails)
        
        if duplicate_count > 0:
            st.warning(f"🔄 মোট {duplicate_count}টি ডুপ্লিকেট ইমেইল স্বয়ংক্রিয়ভাবে বাদ দেওয়া হয়েছে।")
            
        if len(unique_emails) > 0:
            st.info(f"📋 যাচাই করার জন্য মোট ইউনিক ইমেইল পাওয়া গেছে: {len(unique_emails)}টি।")
            
            # Start Bulk Checking Button
            if st.button("🚀 Start Bulk Checking", use_container_width=True):
                
                # প্রগ্রেস বার ও লাইভ কাউন্টার
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # লাইভ ডাটা দেখানোর জন্য খালি কন্টেইনার
                table_placeholder = st.empty()
                
                results = []
                active_list = []
                inactive_list = []
                invalid_list = []
                
                # চেকিং লুপ শুরু
                for idx, email in enumerate(unique_emails):
                    status = check_gmail(email)
                    results.append({"Email": email, "Status": status})
                    
                    if status == "Active/Exist":
                        active_list.append(email)
                    elif status == "Does Not Exist":
                        inactive_list.append(email)
                    else:
                        invalid_list.append(email)
                        
                    # লাইভ প্রগ্রেস আপডেট
                    progress = (idx + 1) / len(unique_emails)
                    progress_bar.progress(progress)
                    status_text.markdown(f"**চেক করা হচ্ছে:** `{idx+1}/{len(unique_emails)}` | **চলতি ইমেইল:** `{email}` -> *{status}*")
                    
                    # প্রগতিশীল টেবিল আপডেট
                    df_live = pd.DataFrame(results)
                    table_placeholder.dataframe(df_live, use_container_width=True, height=250)
                    
                    # প্রিমিয়াম সেফটি ডিলে
                    time.sleep(delay_time)
                
                status_text.success("🎉 চেকিং সফলভাবে সম্পন্ন হয়েছে!")
                
                # ড্যাশবোর্ড স্ট্যাটাস কার্ডস
                st.write("### 📊 সামগ্রিক রিপোর্ট (Summary Report)")
                c1, c2, c3 = st.columns(3)
                c1.metric("সক্রিয় জিমেইল (Active)", f"{len(active_list)}টি")
                c2.metric("অস্তিত্বহীন (Does Not Exist)", f"{len(inactive_list)}টি")
                c3.metric("ভুল ফরম্যাট/ব্লকড", f"{len(invalid_list)}টি")
                
                # ডাউনলোড সেকশন (Premium multi-button layout)
                st.write("### 📥 ডেটা ডাউনলোড করুন")
                dl1, dl2 = st.columns(2)
                
                if active_list:
                    active_txt = "\n".join(active_list)
                    dl1.download_button(
                        label="📥 ডাউনলোড করুন সক্রিয় ইমেইল (.txt)",
                        data=active_txt,
                        file_name="active_gmails.txt",
                        mime="text/plain",
                        key="dl_act"
                    )
                
                if inactive_list:
                    inactive_txt = "\n".join(inactive_list)
                    dl2.download_button(
                        label="📥 ডাউনলোড করুন নিষ্ক্রিয় ইমেইল (.txt)",
                        data=inactive_txt,
                        file_name="inactive_gmails.txt",
                        mime="text/plain",
                        key="dl_inact"
                    )
        else:
            st.error("ফাইলটির ভেতরে কোনো ইমেইল পাওয়া যায়নি!")

# --- মোড ২: সিঙ্গেল ইমেইল চেক ---
elif mode == "Single Email Check":
    st.subheader("🔍 একক জিমেইল ভ্যালিডেটর")
    single_email = st.text_input("একটি জিমেইল অ্যাড্রেস লিখুন:", placeholder="username@gmail.com")
    
    if st.button("Check Single Email", use_container_width=True):
        if single_email.strip():
            with st.spinner("সার্ভারের সাথে কানেক্ট করা হচ্ছে..."):
                status = check_gmail(single_email.strip())
                
            if status == "Active/Exist":
                st.success(f"✅ **{single_email}** - এই জিমেইল অ্যাকাউন্টটি সক্রিয় এবং ব্যবহারযোগ্য।")
            elif status == "Does Not Exist":
                st.error(f"❌ **{single_email}** - এই জিমেইলটির কোনো অস্তিত্ব নেই বা ডিলিট করা হয়েছে।")
            elif status == "Invalid Format":
                st.warning(f"⚠️ **{single_email}** - ইমেইলের ফরম্যাট সঠিক নয়। শেষে অবশ্যই @gmail.com থাকতে হবে।")
            else:
                st.info(f"ℹ️ রেসপন্স: {status}. গুগল সার্ভার থেকে সাময়িক বাধা দিচ্ছে। একটু পর ট্রাই করুন।")
        else:
            st.warning("অনুগ্রহ করে একটি ইমেইল ইনপুট দিন।")

# ফুটার
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Premium Real-time Validation Engine powered by Python & Streamlit</p>", unsafe_allow_html=True)
