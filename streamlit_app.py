import streamlit as st
import requests
from datetime import time, datetime  # Fixed import
import threading
import time as time_module  # Renamed to avoid conflict



def auth_section():
    st.markdown("""
    <style>
      .auth-box {
          background-color: transparent;
          padding: 2rem 1rem 1rem;
          border-radius: 1rem;
          max-width: 500px;
          margin: auto;
      }
      .auth-header {
          text-align: center;
          margin-bottom: 1.5rem;
      }
      .auth-title {
          font-size: 2.5rem;
          font-weight: 600;
          margin: 0;
      }
      .welcome-text {
          color: #ffffff;
      }
      .app-name {
          color: #6c63ff;
      }
      .auth-subtitle {
          color: #cccccc;
          font-size: 1rem;
          margin-top: 0.25rem;
      }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
    st.markdown("""
      <div class='auth-header'>
        <h2 class='auth-title'>
          <span class='welcome-text'>Welcome to</span>
          <span class='app-name'>HealthPal</span>
        </h2>
        <p class='auth-subtitle'>Your trusted AI health companion</p>
      </div>
    """, unsafe_allow_html=True)

    tab_login, tab_register = st.tabs(["🔓 Login", "📝 Register"])

    with tab_login:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log In", use_container_width=True):
            if not username or not password:
                st.warning("Please fill in both fields.")
            else:
                res = requests.post(
                    "http://localhost:8000/login",
                    json={"username": username, "password": password}
                )
                if res.status_code == 200:
                    user_data = res.json()
                    # Debug information
                    st.write("Debug - Login Response:", user_data)
                    
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.full_name = user_data.get('full_name', 'Not provided')
                    st.session_state.age = user_data.get('age', 'Not provided')
                    st.session_state.email = user_data.get('email', 'Not provided')
                    
                    # Debug information
                    st.write("Debug - Session State:", {
                        'full_name': st.session_state.get('full_name'),
                        'age': st.session_state.get('age'),
                        'email': st.session_state.get('email')
                    })
                    
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")

    with tab_register:
        full_name = st.text_input("Full Name", key="reg_name")
        age = st.number_input("Age", min_value=1, max_value=120, value=18, key="reg_age")
        email = st.text_input("Email", key="reg_email")
        new_user = st.text_input("Username", key="reg_user", 
                                help="Username must be at least 5 characters long")
        new_pass = st.text_input("Password", type="password", key="reg_pass", 
                                help="Password must be at least 8 characters long")
        
        if st.button("Register", use_container_width=True):
            if not new_user or not new_pass or not full_name:
                st.warning("Please fill in all required fields.")
            elif len(new_user) < 5:
                st.error("Username must be at least 5 characters long.")
            elif len(new_pass) < 8:
                st.error("Password must be at least 8 characters long.")
            else:
                try:
                    res = requests.post(
                        "http://localhost:8000/register",
                        json={
                            "username": new_user,
                            "password": new_pass,
                            "full_name": full_name,
                            "age": age,
                            "email": email
                        }
                    )
                    response_data = res.json()
                    
                    if response_data.get("status") == "success":
                        st.success("Registered successfully! You can now log in.")
                    else:
                        st.error(response_data.get("detail", "Registration failed"))
                except Exception as e:
                    st.error(f"Registration failed: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)



st.set_page_config(page_title="HealthPal", page_icon="💊")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    auth_section()
    st.stop()

if "logged_in" in st.session_state and st.session_state.logged_in:
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: #6c63ff; font-size: 2rem; margin: 0;'>HealthPal</h1>
            <p style='color: #cccccc; margin: 0.5rem 0;'>Your trusted AI health companion</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
        # User Profile Section
        st.markdown(f"### 👤 {st.session_state.get('username', 'User')}")
        st.markdown(f"""
        **Name:** {st.session_state.get('full_name', 'Not provided')}  
        **Age:** {st.session_state.get('age', 'Not provided')}  
        **Email:** {st.session_state.get('email', 'Not provided')}
        """)
        
        st.markdown("---")
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.clear()
            st.rerun()



# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you with medical questions today?"}]

if "reminders" not in st.session_state:
    st.session_state.reminders = []

if "medical_history" not in st.session_state:
    st.session_state.medical_history = []

# --- Reminder Scheduler Thread ---
def check_reminders():
    while True:
        now = datetime.now().strftime("%H:%M")
        today = datetime.now().strftime("%a")
        
        for reminder in st.session_state.reminders:
            if now == reminder["time"] and today in reminder["days"]:
                st.toast(f"⏰ Reminder: Take {reminder['dosage']} of {reminder['medication']}", icon="💊")
        
        time_module.sleep(60)  # Check every minute

# Start scheduler thread
if not hasattr(st.session_state, 'scheduler_thread'):
    st.session_state.scheduler_thread = threading.Thread(target=check_reminders, daemon=True)
    st.session_state.scheduler_thread.start()

# --- App Layout ---
tab1, tab2, tab3 = st.tabs(["Medical Chatbot", "Medication Reminder", "Medical History"])

with tab1:
    st.header("💬 Medical Chatbot")
    st.write("Ask me anything about general health, symptoms, or medications.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            response = requests.post("http://localhost:8000/chat", json={"text": prompt}, timeout=10)
            reply = response.json().get("reply", "⚠️ No response from server")
        except requests.exceptions.RequestException as e:
            reply = f"❌ Error: {str(e)}"

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

with tab2:
    # --- Medication Reminder Interface ---
    st.header("💊 Medication Reminder")
    
    with st.expander("➕ Add New Reminder"):
        with st.form("reminder_form"):
            med = st.text_input("Medication Name", placeholder="e.g., Ibuprofen")
            dose = st.text_input("Dosage", placeholder="e.g., 200mg")
            reminder_time = st.time_input("Time", value=time(8, 0))
            notes = st.text_area("Additional Notes", placeholder="Any additional information")
            days = st.multiselect(
                "Repeat Days",
                ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                default=["Mon", "Wed", "Fri"]
            )
            
            if st.form_submit_button("Set Reminder"):
                new_reminder = {
                    "medication": med,
                    "dosage": dose,
                    "time": reminder_time.strftime("%H:%M"),
                    "days": days,
                    "notes": notes
                }
                st.session_state.reminders.append(new_reminder)
                st.success(f"Reminder set for {reminder_time.strftime('%I:%M %p')} on {', '.join(days)}")
                st.rerun()
    
    # Display current reminders
    st.subheader("Your Active Reminders")
    if not st.session_state.reminders:
        st.info("No reminders set yet")
    else:
        # Sort reminders by time
        sorted_reminders = sorted(st.session_state.reminders, key=lambda x: x['time'])
        
        for i, reminder in enumerate(sorted_reminders):
            with st.expander(f"**{reminder['medication']}**"):
                st.markdown(f"""
                **Dosage:** {reminder['dosage']}  
                **Time:** {reminder['time']}  
                **Days:** {', '.join(reminder['days'])}  
                **Notes:** {reminder.get('notes', '-')}
                """)
                if st.button("Delete Reminder", key=f"delete_{i}"):
                    st.session_state.reminders.pop(i)
                    st.rerun()

with tab3:
    st.header("📋 Medical History")
    
    with st.expander("➕ Add New Medical Record"):
        with st.form("medical_history_form"):
            record_type = st.selectbox(
                "Record Type",
                ["Condition", "Allergy", "Surgery", "Vaccination", "Other"]
            )
            description = st.text_area("Description", placeholder="Enter details about your medical record")
            date = st.date_input("Date", value=datetime.now().date())
            notes = st.text_area("Additional Notes", placeholder="Any additional information")
            
            if st.form_submit_button("Add Record"):
                new_record = {
                    "type": record_type,
                    "description": description,
                    "date": date.strftime("%Y-%m-%d"),
                    "notes": notes
                }
                st.session_state.medical_history.append(new_record)
                st.success("Medical record added successfully!")
    
    # Display medical history
    st.subheader("Your Medical Records")
    if not st.session_state.medical_history:
        st.info("No medical records added yet")
    else:
        for i, record in enumerate(st.session_state.medical_history):
            with st.expander(f"**{record['type']}**   -   **{record['date']}**"):
                st.markdown(f"""
                **Description:** {record['description']}  
                **Date:** {record['date']}  
                **Notes:** {record.get('notes', '-')}
                """)
                if st.button("Delete Record", key=f"delete_record_{i}"):
                    st.session_state.medical_history.pop(i)
                    st.rerun()

# --- Run the App ---
if __name__ == "__main__":
    # st.info("Note: The FastAPI backend must be running at http://localhost:8000")
    st.info("HealthPal")