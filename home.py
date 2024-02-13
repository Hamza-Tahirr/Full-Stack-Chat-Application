import streamlit as st

st.set_page_config(
    page_title="Introduction",
    page_icon="👋",
)

from langchain.chains.conversation.memory import ConversationBufferWindowMemory

# """
# Initialising session states  
# """
if 'openai_api_key' not in st.session_state:
    st.session_state['openai_api_key'] = None

if 'pinecone_api_key' not in st.session_state:
    st.session_state['pinecone_api_key'] = None

if 'pinecone_env' not in st.session_state:
    st.session_state['pinecone_env'] = None

if 'pinecone_index_namespace' not in st.session_state:
    st.session_state['pinecone_index_namespace'] = None

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)


# """
# Page Content  
# """
st.write("# Welcome to ChatPDF! 👋")

st.markdown(
"""
ChatPDF is a user-friendly software that allows you to ask questions 
and get answers from your personal and organizational documents. 
This software uses OpenAI ChatGPT to query documents and Pinecone Vector Database to store documents.
How to use:
1. Make an accout on [OpenAI](https://platform.openai.com/) and [Pinecone](https://www.pinecone.io/).
2. Enter your credentials. This include OpenAI API Key, Pinecone API Key, Pinecone Environment and Pinecone Index Name.
3. Upload Documents. These documents will be uploaded to Pinecone Database.
4. Chat with your documents. Chatbot is built on top of ChatGPT Engine.
"""
)