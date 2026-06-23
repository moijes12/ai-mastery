import requests
import streamlit as st

st.set_page_config(page_title="SupportFlow", layout="wide")
st.title("🚀 SupportFlow - Intelligent Customer Support")

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Submit Ticket", "Dashboard"])

if page == "Submit Ticket":
    st.header("Create New Support Ticket")
    subject = st.text_input("Subject")
    description = st.text_area("Description", height=150)

    if st.button("Submit Ticket"):
        if subject and description:
            try:
                response = requests.post(
                    "http://backend:8000/api/v1/tickets/",
                    json={"subject": subject, "description": description},
                )
                if response.status_code == 200:
                    st.success("Ticket submitted successfully!")
                else:
                    st.error("Failed to submit ticket")
            except Exception as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Please fill in all fields")

elif page == "Dashboard":
    st.header("Analytics Dashboard")
    st.info("Dashboard coming soon... (We'll build this after ML integration)")
