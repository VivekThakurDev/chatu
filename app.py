import streamlit as st
import requests
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client for NVIDIA API
# Assuming the API key is set in the Nvd_API environment variable
nvidia_api_key = os.getenv("Nvd_API")

if not nvidia_api_key:
    st.error("Error: Nvd_API environment variable not found. Please check your .env file.")
    st.stop()

# Configure the client to point to NVIDIA's base URL
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=nvidia_api_key
)

# Set the page title and configuration
st.set_page_config(page_title="NVIDIA AI Chat", page_icon="⚡", layout="centered", initial_sidebar_state="collapsed")

# Inject Premium Chat App CSS
st.markdown("""
<style>
/* Main Background and Text */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #1a1a24 0%, #09090b 100%);
    color: #fafafa;
    font-family: 'Inter', sans-serif;
}
/* Hide Streamlit top header and deploy button */
[data-testid="stHeader"] {
    visibility: hidden;
    background: transparent;
}
/* General container adjustments */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 5rem !important;
}
/* Chat message bubbles with animation and contrast fix */
@keyframes slideUp {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}
[data-testid="stChatMessage"] {
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 10px -1px rgba(0, 0, 0, 0.2);
    background: rgba(30, 30, 36, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
    animation: slideUp 0.4s ease-out forwards;
    transition: background 0.3s, border 0.3s;
}
[data-testid="stChatMessage"] * {
    color: #fafafa !important;
}
[data-testid="stChatMessage"]:hover {
    background: rgba(40, 40, 46, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.15);
}
/* Avatars */
[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, #10b981, #059669);
}
/* Chat input pinning & styling - Fix for the white box */
[data-testid="stBottom"] > div {
    background: transparent !important;
}
[data-testid="stBottom"] {
    background: transparent !important;
}
[data-testid="stChatInput"] {
    background: rgba(20, 20, 24, 0.95) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.7) !important;
    backdrop-filter: blur(15px) !important;
}
/* Fix Text Color in Chat Input Box */
textarea {
    color: #ffffff !important;
}
[data-testid="stChatInputTextArea"] {
    color: #ffffff !important;
}
/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: rgba(12, 12, 14, 0.95) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}
hr {
    border-color: rgba(255, 255, 255, 0.1);
}
</style>
""", unsafe_allow_html=True)

# Custom Title Header
st.markdown("<h2 style='text-align: center; font-weight: 800; background: -webkit-linear-gradient(45deg, #10b981, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>⚡ Next-Gen Chat AI</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a1a1aa; font-size: 0.9rem; margin-bottom: 2rem;'>Powered by Nvidia Llama 3.1</p>", unsafe_allow_html=True)

# Sidebar for Image Analysis (Nemotron)
with st.sidebar:
    st.header("🖼️ Nemotron Image Analysis")
    st.markdown("Analyze page elements in images with `nemotron-page-elements-v3`")
    
    uploaded_file = st.file_uploader("Upload an image (PNG/JPG)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        
        if st.button("Analyze Image"):
            with st.spinner("Analyzing..."):
                image_bytes = uploaded_file.getvalue()
                image_b64 = base64.b64encode(image_bytes).decode('utf-8')
                
                if len(image_b64) > 180_000:
                    st.error("Error: To upload larger images (> 180k chars in base64), use the assets API instead. Please upload a smaller image.")
                else:
                    invoke_url = "https://ai.api.nvidia.com/v1/cv/nvidia/nemotron-page-elements-v3"
                    headers = {
                        "Authorization": f"Bearer {nvidia_api_key}",
                        "Accept": "application/json"
                    }
                    
                    file_ext = uploaded_file.name.split('.')[-1].lower()
                    mime_type = "image/jpeg" if file_ext in ['jpg', 'jpeg'] else "image/png"
                    
                    payload = {
                        "input": [
                            {
                                "type": "image_url",
                                "url": f"data:{mime_type};base64,{image_b64}"
                            }
                        ]
                    }
                    
                    try:
                        response = requests.post(invoke_url, json=payload, headers=headers)
                        response.raise_for_status()
                        result = response.json()
                        st.success("Analysis Complete!")
                        st.json(result)
                        
                        # Add system message to describe what happened
                        if "messages" not in st.session_state:
                            st.session_state.messages = []
                        st.session_state.messages.append({"role": "assistant", "content": f"**Nemotron Analysis Result for {uploaded_file.name}:**\n```json\n{result}\n```"})
                        
                    except Exception as e:
                        st.error(f"Failed to analyze image: {e}")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Message the AI..."):
    # Output the user's prompt in the chat interface
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response placeholder
    with st.chat_message("assistant"):
        try:
            # Generate the response using NVIDIA API
            # Note: The model name should be one supported by the Nvidia API base URL you are using.
            stream = client.chat.completions.create(
                model="meta/llama-3.1-8b-instruct",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            
            # st.write_stream efficiently handles rapid streaming tokens 
            # without causing UI lag by batching updates.
            def generate_stream():
                for response in stream:
                    delta_content = response.choices[0].delta.content
                    if delta_content:
                        yield delta_content
            
            full_response = st.write_stream(generate_stream)

        
        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = "Sorry, I ran into an error generating a response."
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
