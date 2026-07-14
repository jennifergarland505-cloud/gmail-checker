import streamlit as st
import pandas as pd
import re

st.title("📧 Gmail Format Checker")

emails = st.text_area("Paste emails (one per line)")

if st.button("Check"):
    regex = r'^[A-Za-z0-9._%+-]+@gmail\.com$'

    data = []

    for email in emails.splitlines():
        email = email.strip()
        if email:
            status = "✅ Valid Format" if re.match(regex, email) else "❌ Invalid Format"
            data.append([email, status])

    if data:
        df = pd.DataFrame(data, columns=["Email", "Status"])
        st.dataframe(df)
