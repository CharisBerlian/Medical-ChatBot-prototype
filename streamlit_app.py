import streamlit as st
import requests
from datetime import time, datetime  # Fixed import
import threading
import time as time_module  # Renamed to avoid conflict

# --- App Configuration ---
st.set_page_config(page_title="Medical Assistant", page_icon="💊")

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
    # --- Chatbot Interface ---
    st.header("🩺 Medical Chatbot")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Your medical question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Call FastAPI backend
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"text": prompt},
                timeout=10
            )
            reply = response.json().get("reply", "No response from server")
        except requests.exceptions.RequestException as e:
            reply = f"Error: {str(e)}"
        
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