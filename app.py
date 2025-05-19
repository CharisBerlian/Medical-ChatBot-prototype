# --- Sidebar CSS Styling (put this near top of file) ---
st.markdown("""
<style>
  /* Sidebar background & text */
  [data-testid="stSidebar"] {
    background-color: #1f1f2e;
    color: #ddd;
  }
  /* Make the sidebar full height */
  .css-1d391kg { min-height: 100vh !important; }
  /* Section headers */
  .sidebar-section h3 {
    margin: 1.2rem 0 0.5rem;
    font-size: 1rem;
    color: #6c63ff;
    border-bottom: 1px solid #333;
    padding-bottom: 0.2rem;
  }
  /* Logout button styling */
  .logout-btn button {
    background-color: #c63f52;
    color: white;
    width: 100%;
    padding: 0.6rem;
    border: none;
    border-radius: 0.4rem;
    margin-top: 1rem;
  }
  .logout-btn button:hover {
    background-color: #a22b3d;
  }
</style>
""", unsafe_allow_html=True)

# --- Enhanced Sidebar ---
with st.sidebar:
    # Account section
    st.markdown("<div class='sidebar-section'><h3>👩‍⚕️ Account</h3></div>", unsafe_allow_html=True)
    st.markdown(f"**{st.session_state.username}**")
    st.markdown("---")
    
    # Navigation
    st.markdown("<div class='sidebar-section'><h3>📋 Navigation</h3></div>", unsafe_allow_html=True)
    page = st.radio(
        "",
        ["Medical Chatbot", "Medication Reminder"],
        index=0,
        label_visibility="collapsed"
    )
    st.markdown("---")
    
    # Settings (placeholder for future options)
    st.markdown("<div class='sidebar-section'><h3>⚙️ Settings</h3></div>", unsafe_allow_html=True)
    # e.g. st.selectbox("Model:", ["GPT-3.5", "GPT-4"], key="model")
    
    # Logout
    st.markdown("<div class='logout-btn'>", unsafe_allow_html=True)
    if st.button("🚪 Log Out"):
        st.session_state.clear()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True) 