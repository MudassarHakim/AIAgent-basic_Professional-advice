import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Configure Gemini (replace with your API key)
genai.configure(api_key="AIzaSyCiggltThVkzNdeiBB2iw-xmM1A2bFZlcM")
model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! 👋\nMy name is Mudassar. Let me help you today"}
    ]
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

# Title and header
st.title("👋 Mudassar here")
st.subheader("Career Advisor Assistant")

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Check if we need to collect user information
    if not st.session_state.user_info:
        # Build the system message from your n8n workflow
        system_message = """To provide you with the most valuable advice, I'd love to understand:

Your current role:
(Individual Contributor/Manager/Director/Executive/Founder)

Years of experience in your field:
(0-3 years | 4-7 years | 8-12 years | 13+ years)

Your biggest professional challenge right now:
(e.g., getting promoted, transitioning to leadership, navigating industry changes, work-life balance)

Please provide this information so I can offer specific strategies for your career stage."""
        
        with st.chat_message("assistant"):
            st.markdown(system_message)
        st.session_state.messages.append({"role": "assistant", "content": system_message})
    else:
        # Process the message with Gemini
        # Include conversation history for context
        chat_history = "\n".join(
            f"{msg['role']}: {msg['content']}" 
            for msg in st.session_state.messages[-6:]  # Last 6 messages as memory buffer
        )
        
        # Generate response
        response = model.generate_content(
            f"Conversation history:\n{chat_history}\n\nUser's information:\n{st.session_state.user_info}\n\nRespond to the user's latest message: {prompt}"
        )
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# User information collection form (alternative approach)
with st.expander("Provide Your Information (Optional)"):
    with st.form("user_info_form"):
        role = st.selectbox(
            "Your current role",
            ["Individual Contributor", "Manager", "Director", "Executive", "Founder"]
        )
        experience = st.selectbox(
            "Years of experience",
            ["0-3 years", "4-7 years", "8-12 years", "13+ years"]
        )
        challenge = st.text_area("Your biggest professional challenge right now")
        
        if st.form_submit_button("Submit Information"):
            st.session_state.user_info = {
                "role": role,
                "experience": experience,
                "challenge": challenge
            }
            st.success("Information saved! Now I can provide more tailored advice.")
