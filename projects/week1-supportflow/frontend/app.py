import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SupportFlow", layout="wide")
st.title("🚀 SupportFlow - Intelligent Customer Support Platform")

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Select Page", ["Submit Ticket", "View Tickets", "Dashboard"])

BASE_URL = "http://support-flow-backend:8000/api/v1"  # Use service name if inside Docker network

if page == "Submit Ticket":
    st.header("Create New Support Ticket")

    with st.form("ticket_form"):
        subject = st.text_input("Subject")
        description = st.text_area("Description", height=150)
        submitted = st.form_submit_button("Submit Ticket")

        if submitted and subject and description:
            try:
                response = requests.post(
                    f"{BASE_URL}/tickets/",
                    json={"subject": subject, "description": description},
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Ticket #{data['id']} created successfully!")
                    st.json(data)
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

elif page == "View Tickets":
    st.header("All Tickets")
    try:
        response = requests.get(f"{BASE_URL}/tickets/")
        if response.status_code == 200:
            tickets = response.json()
            if tickets:
                df = pd.DataFrame(tickets)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No tickets yet.")
        else:
            st.error("Failed to fetch tickets")
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")

elif page == "Dashboard":
    st.header("Analytics Dashboard")
    st.info(
        "📊 Dashboard features coming in the next iteration (after more ML models)."
    )
    st.caption("Currently showing basic prediction capabilities.")

st.caption("SupportFlow v0.1.0 | Backend Status: Connected")
