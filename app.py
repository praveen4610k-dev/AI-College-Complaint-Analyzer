import streamlit as st
import joblib
import pandas as pd
from datetime import datetime
import os

# -------------------------------
# Load ML Model & Vectorizer
# -------------------------------
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# -------------------------------
# Helper Functions
# -------------------------------
def predict_category(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]

def assign_priority(text):
    text = text.lower()
    if any(word in text for word in ["urgent", "immediately", "danger", "no water", "broken","bad","worst"]):
        return "High"
    elif any(word in text for word in ["delay", "late", "not working"]):
        return "Medium"
    else:
        return "Low"

def map_department(category):
    mapping = {
        "Hostel": "Hostel Office",
        "Academic": "Academic Department",
        "Transport": "Transport Office",
        "Infrastructure": "Maintenance",
        "Administration": "Admin Office"
    }
    return mapping.get(category, "General Office")

def save_complaint(complaint, category, department, priority):
    data = {
        "Complaint": complaint,
        "Category": category,
        "Department": department,
        "Priority": priority,
        "Status": "Pending",
        "Submitted_Date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    file = "complaints.csv"
    if os.path.exists(file):
        df = pd.read_csv(file)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])

    df.to_csv(file, index=False)

# -------------------------------
# STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="AI-Based College Complaint Analyzer")

st.title("AI-Based College Complaint Analyzer")

tab1, tab2 = st.tabs(["User", "Admin"])

# -------------------------------
# USER TAB (ONLY SUBMIT)
# -------------------------------
with tab1:
    st.subheader("Submit Complaint")

    with st.form("user_form"):
        complaint = st.text_area("Enter your complaint")
        submit = st.form_submit_button("Submit Complaint")

    if submit:
        if complaint.strip() == "":
            st.warning("Please enter a complaint")
        else:
            category = predict_category(complaint)
            department = map_department(category)
            priority = assign_priority(complaint)

            save_complaint(complaint, category, department, priority)

            st.success("Complaint submitted successfully")
            st.info("Your complaint has been forwarded to the admin")

# -------------------------------
# ADMIN TAB (VIEW OUTPUT)
# -------------------------------
with tab2:
    st.subheader("Admin Login")

    with st.form("admin_form"):
        admin_password = st.text_input("Enter Admin Password", type="password")
        login = st.form_submit_button("Login")

    if login:
        if admin_password == "admin123":
            st.success("Admin login successful")

            if os.path.exists("complaints.csv"):
                df = pd.read_csv("complaints.csv")
                df = df.sort_values(by="Submitted_Date",ascending=False)

                st.subheader("Complaint Analysis Results")

                st.dataframe(
                    df[[
                        "Category",
                        "Department",
                        "Priority",
                        "Status",
                        "Submitted_Date"
                    ]]
                )
            else:
                st.info("No complaints submitted yet")
        else:
            st.error("Incorrect password")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8501))
    import streamlit.web.cli as stcli
    import sys
    sys.argv = ["streamlit", "run", "app.py", "--server.port", str(port), "--server.address", "0.0.0.0"]
    sys.exit(stcli.main())