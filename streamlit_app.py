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
        <p class='auth-subtitle'>Your trusted AI health companion 💊</p>
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
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")

    with tab_register:
        new_user = st.text_input("Username", key="reg_user")
        new_pass = st.text_input("Password", type="password", key="reg_pass")
        if st.button("Register", use_container_width=True):
            if not new_user or not new_pass:
                st.warning("Please fill in both fields.")
            else:
                res = requests.post(
                    "http://localhost:8000/register",
                    json={"username": new_user, "password": new_pass}
                )
                if res.status_code == 200:
                    st.success("🎉 Registered successfully! You can now log in.")
                else:
                    st.error(res.json().get("detail", "Registration failed"))

    st.markdown("</div>", unsafe_allow_html=True)



st.set_page_config(page_title="HealthPal", page_icon="💊")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    auth_section()
    st.stop()

if "logged_in" in st.session_state and st.session_state.logged_in:
    with st.sidebar:
        st.write(f"Logged in as: **{st.session_state.username}**")
        st.markdown("---")
        if st.button("🚪 Log Out"):
            st.session_state.clear()
            st.rerun()



# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you with medical questions today?"}]

if "reminders" not in st.session_state:
    st.session_state.reminders = []

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
tab1, tab2 = st.tabs(["Medical Chatbot", "Medication Reminder"])

with tab1:
    st.header("🩺 Medical Chatbot")
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
            reminder_time = st.time_input("Time", value=time(8, 0))  # Fixed: uses datetime.time
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
                    "days": days
                }
                st.session_state.reminders.append(new_reminder)
                st.success(f"Reminder set for {reminder_time.strftime('%I:%M %p')} on {', '.join(days)}")
    
    # Display current reminders
    st.subheader("Your Active Reminders")
    if not st.session_state.reminders:
        st.info("No reminders set yet")
    else:
        for i, reminder in enumerate(st.session_state.reminders):
            cols = st.columns([3, 1])
            with cols[0]:
                st.markdown(f"""
                **{reminder['medication']}**  
                Dosage: {reminder['dosage']}  
                Time: {reminder['time']}  
                Days: {', '.join(reminder['days'])}
                """)
            with cols[1]:
                if st.button("❌", key=f"delete_{i}"):
                    st.session_state.reminders.pop(i)
                    st.rerun()

# --- Run the App ---
if __name__ == "__main__":
    st.info("Note: The FastAPI backend must be running at http://localhost:8000")