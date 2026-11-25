import os
import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="PY-W4-004 Admin Dashboard", page_icon="📁", layout="wide")
st.title("Enterprise Workflow Automation Dashboard")
st.caption("Authenticated dashboard connected to the FastAPI backend.")
API_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

if "api_token" not in st.session_state:
    st.session_state.api_token = ""

if not st.session_state.api_token:
    with st.form("login_form"):
        st.subheader("Sign in")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
    if submitted:
        try:
            response = requests.post(
                f"{API_URL}/auth/login",
                data={"username": username, "password": password},
                timeout=10,
            )
            if response.ok:
                st.session_state.api_token = response.json()["access_token"]
                st.rerun()
            else:
                st.error("Login failed. Check your username and password.")
        except requests.RequestException as exc:
            st.error(f"Could not connect to the API at {API_URL}: {exc}")
    st.info("Start the FastAPI server first. Register the first account through /docs to create the local admin account.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.api_token}"}

def api_get(path):
    response = requests.get(f"{API_URL}{path}", headers=headers, timeout=15)
    if response.status_code == 401:
        st.session_state.api_token = ""
        st.error("Your session expired. Please log in again.")
        st.stop()
    response.raise_for_status()
    return response.json()

try:
    summary = api_get("/reports/summary")
    employees = api_get("/employees")
    documents = api_get("/documents")
    workflows = api_get("/workflows")
except requests.RequestException as exc:
    st.error(f"Unable to load dashboard data: {exc}")
    if st.button("Log out"):
        st.session_state.api_token = ""
        st.rerun()
    st.stop()

if st.button("Log out"):
    st.session_state.api_token = ""
    st.rerun()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Employees", summary.get("total_employees", 0))
c2.metric("Documents", summary.get("total_documents", 0))
c3.metric("Pending approvals", summary.get("workflows", {}).get("Pending", 0))
c4.metric("Approved", summary.get("workflows", {}).get("Approved", 0))

st.subheader("Employees")
search = st.text_input("Search employees by name, code, or email")
employee_rows = [
    {"Code": e["employee_code"], "Name": e["name"], "Email": e["email"],
     "Job title": e.get("job_title", ""), "Status": e["status"], "Department ID": e.get("department_id")}
    for e in employees
]
if search:
    term = search.lower()
    employee_rows = [row for row in employee_rows if term in " ".join(str(v) for v in row.values()).lower()]
employee_frame = pd.DataFrame(employee_rows)
st.dataframe(employee_frame, use_container_width=True)
if not employee_frame.empty:
    st.download_button("Download employee CSV", employee_frame.to_csv(index=False), "employees.csv", "text/csv")

st.subheader("Workflow queue")
workflow_frame = pd.DataFrame([{"ID": w["id"], "Title": w["title"], "Status": w["status"], "Created": w["created_at"]} for w in workflows])
st.dataframe(workflow_frame, use_container_width=True)

st.subheader("Documents")
document_frame = pd.DataFrame([{"ID": d["id"], "File": d["original_name"], "Category": d["category"], "Size (bytes)": d["size_bytes"]} for d in documents])
st.dataframe(document_frame, use_container_width=True)

st.subheader("Department summary")
st.dataframe(pd.DataFrame([{"Department": name, "Employees": count} for name, count in summary.get("departments", {}).items()]), use_container_width=True)
