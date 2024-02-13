import streamlit as st

st.set_page_config(
    page_title="Credentials",
    page_icon="🔐",
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

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)

st.write("# Enter your Credentials! 🔐")

# """
# Page Content  
# """
st.markdown(
"""
Enter the following credentials to start uploading and querying documents.
"""
)

# OpenAI API Key input
openai_api_key = st.text_input("Enter your OpenAI API Key", type='password')
if openai_api_key:
    # Use the OpenAI API key (e.g., validate it, make a request to an API, etc.)
    st.session_state['openai_api_key'] = openai_api_key
    
# Pinecone API Key input
pinecone_api_key = st.text_input("Enter your Pinecone API Key", type='password')
if pinecone_api_key:
    st.session_state['pinecone_api_key'] = pinecone_api_key

# Pinecone Environment input
pinecone_env = st.text_input("Enter your Pinecone Environment", type='password')
if pinecone_env:
    st.session_state['pinecone_env'] = pinecone_env

# Index Namespace input
pinecone_index_namespace = st.text_input("Enter your Pinecone Index Namespace", type='password')
if pinecone_index_namespace:
    st.session_state['pinecone_index_namespace'] = pinecone_index_namespace

# Check if all required fields are filled
all_fields_filled = all([st.session_state['pinecone_api_key'], 
                         st.session_state['openai_api_key'], 
                         st.session_state['pinecone_env'], 
                         st.session_state['pinecone_index_namespace']])

if all_fields_filled:
    st.success('Credentials Stored')