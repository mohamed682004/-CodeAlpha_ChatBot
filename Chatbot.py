import streamlit as st
from langchain_community.llms import Ollama
from PIL import Image
import time

# Initialize the Ollama model
llm = Ollama(model='qwen:0.5b')

# Configure the page
st.set_page_config(
    page_title="Chatbot Using Qwen",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    /* Main container */
    .main {
        background-color: #1E1E1E;
        padding: 2rem;
        border-radius: 15px;
    }
    
    /* Header styling */
    .title {
        text-align: center;
        color: #FFFFFF;
        font-size: 3rem !important;
        margin-bottom: 2rem !important;
        background: linear-gradient(45deg, #2196F3, #00BCD4);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background-color: #2D2D2D !important;
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        border: 2px solid #4CAF50 !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(45deg, #4CAF50, #45a049) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 0.8rem 2rem !important;
        font-size: 1.2rem !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
        width: 200px !important;
        margin: 0 auto !important;
        display: block !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Response container */
    .response-container {
        background-color: #2D2D2D;
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 2rem;
        border-left: 5px solid #4CAF50;
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1E1E1E;
        text-align: center;
        padding: 1rem;
        font-size: 1rem;
        color: #FFFFFF;
        border-top: 2px solid #4CAF50;
    }
    
    /* Chat history */
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        animation: fadeIn 0.5s ease-in;
    }
    
    .user-message {
        background-color: #2D2D2D;
        border-left: 5px solid #2196F3;
    }
    
    .bot-message {
        background-color: #2D2D2D;
        border-left: 5px solid #4CAF50;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Title
st.markdown('<h1 class="title">🤖 Chatbot Using Qwen 🚀</h1>', unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    # Chat input
    prompt = st.text_area("💬 Enter your message here:", height=150, key="input")
    
    # Submit button
    if st.button("🚀 Submit", key="submit"):
        if prompt:
            # Add user message to chat history
            st.session_state.chat_history.append(("user", prompt))
            
            with st.spinner("🤔 Thinking..."):
                try:
                    # Generate response
                    response = llm.invoke(prompt, stop=['<|eot-id|>'])
                    # Add bot response to chat history
                    st.session_state.chat_history.append(("bot", response))
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a message!")

with col2:
    # Display chat statistics
    st.markdown("""
    ### 📊 Chat Statistics
    """)
    if st.session_state.chat_history:
        st.info(f"Total Messages: {len(st.session_state.chat_history)}")
        user_msgs = len([msg for msg in st.session_state.chat_history if msg[0] == "user"])
        st.info(f"Your Messages: {user_msgs}")
        st.info(f"Bot Messages: {len(st.session_state.chat_history) - user_msgs}")

# Display chat history
st.markdown("### 💬 Chat History")
for role, message in st.session_state.chat_history:
    if role == "user":
        st.markdown(f'<div class="chat-message user-message">👤 You: {message}</div>', 
                   unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message bot-message">🤖 Bot: {message}</div>', 
                   unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        Made by <b>Mohamed</b> for <b>Code Alpha</b>
    </div>
""", unsafe_allow_html=True)

# Add clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()  # Using st.rerun() instead of st.experimental_rerun()