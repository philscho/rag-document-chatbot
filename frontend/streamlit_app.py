import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("📄 Master's thesis chatbot")
st.caption("Ask questions about my master's thesis!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/query",
                    json={"question": prompt}
                )
                response.raise_for_status()
                answer = response.json()["answer"]
            except requests.exceptions.ConnectionError:
                answer = "❌ Could not connect to API. Is it running?"
            except Exception as e:
                answer = f"❌ Error: {str(e)}"
    
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
