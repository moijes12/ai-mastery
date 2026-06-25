from datetime import datetime

import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="SupportFlow", layout="wide")
st.title("🚀 SupportFlow - Intelligent Customer Support Platform")

# Configuration
BASE_URL = "http://support-flow-backend:8000/api/v1"

st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Submit Ticket", "View Tickets", "Dashboard"])

if page == "Submit Ticket":
    st.header("Create New Support Ticket")

    with st.form("ticket_form", clear_on_submit=True):
        subject = st.text_input("Subject", placeholder="Laptop keeps crashing...")
        description = st.text_area(
            "Description", height=150, placeholder="Describe the issue in detail..."
        )

        submitted = st.form_submit_button("Submit Ticket & Get AI Analysis")

        if submitted and subject and description:
            with st.spinner("AI is analyzing ticket..."):
                try:
                    response = requests.post(
                        f"{BASE_URL}/tickets/",
                        json={"subject": subject, "description": description},
                    )

                    if response.status_code == 200:
                        ticket = response.json()
                        st.success(f"✅ Ticket #{ticket['id']} created successfully!")

                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Predicted Category", ticket["category"])
                            st.metric("Urgency", ticket["urgency"])
                        with col2:
                            st.metric(
                                "Est. Resolution Time",
                                f"{ticket['predicted_resolution_time_hours']} hours",
                            )
                            st.metric(
                                "Priority Score", f"{ticket['priority_score']}/100"
                            )

                        st.json(ticket)
                    else:
                        st.error(f"Failed: {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

elif page == "View Tickets":
    st.header("All Support Tickets")
    try:
        response = requests.get(f"{BASE_URL}/tickets/")
        if response.status_code == 200:
            tickets = response.json()
            if tickets:
                df = pd.DataFrame(tickets)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No tickets yet. Create some above!")
        else:
            st.error("Failed to load tickets")
    except Exception as e:
        st.error(f"Could not connect to backend: {e}")

elif page == "Dashboard":
    st.header("Analytics Dashboard")
    st.info("📊 Full dashboard with charts coming soon (after we add more evaluation)")
    st.caption("Current capabilities: AI-powered ticket classification & prediction")

st.caption(
    f"SupportFlow v0.1.0 | Backend Connected @ {datetime.now().strftime('%H:%M')}"
)
