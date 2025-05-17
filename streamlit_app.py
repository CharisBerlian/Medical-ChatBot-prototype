import streamlit as st
import requests

st.title("Medical Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you with medical questions today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Your medical question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Call your FastAPI backend
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"text": prompt}
        )
        reply = response.json()["reply"]
    except Exception as e:
        reply = f"Error: {str(e)}"
    
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})