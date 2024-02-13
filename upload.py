import streamlit as st

st.set_page_config(
    page_title="Upload Documents",
    page_icon="📄",
)

from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from utils import ingest

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


# """
# Page Content  
# """
st.write("# Upload your Documents! 📄")

# Check if all required fields are filled
all_fields_filled = all([st.session_state['pinecone_api_key'], 
                         st.session_state['openai_api_key'], 
                         st.session_state['pinecone_env'], 
                         st.session_state['pinecone_index_namespace']])

if not all_fields_filled:
    st.error('Credentials 🔐 not found. Enter Credentials 🔐 to activate uploader')
    uploaded_file = st.file_uploader("Upload Document", type=['pdf'], disabled=True)

else:
    uploaded_file = st.file_uploader("Upload Document", type=['pdf', 'docx'], disabled=False)
    if uploaded_file:
        ingest(uploaded_file, 
               pinecone_api_key=st.session_state['pinecone_api_key'],
               pinecone_env=st.session_state['pinecone_env'],
               pinecone_index_namespace=st.session_state['pinecone_index_namespace']
               )