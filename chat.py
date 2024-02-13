import streamlit as st

st.set_page_config(
    page_title="Chatbot",
    page_icon="📄",
)

from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from utils import *

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

system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
and if the answer is not contained within the text below, say 'I don't know'""")

human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

empty_openai_api_key = False

try:
    openai.api_key = st.session_state['openai_api_key']
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=st.session_state['openai_api_key'])
    conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)
except Exception as e:
    print(e)
    empty_openai_api_key = True

# """
# Page Content  
# """
st.write("# Chat with your Documents! 🤖")

if empty_openai_api_key:
    st.error('Enter OpenAI API key in credentials tab')

else:
    try:
        # container for chat history
        response_container = st.container()
        # container for text box
        textcontainer = st.container()


        with textcontainer:
            query = st.text_input("Query: ", key="input")
            if query:
                with st.spinner("typing..."):
                    conversation_string = get_conversation_string()
                    refined_query = query_refiner(conversation_string, query)
                    context = find_match(refined_query,
                                        pinecone_api_key=st.session_state['pinecone_api_key'],
                                        pinecone_env=st.session_state['pinecone_env'],
                                        pinecone_index_namespace=st.session_state['pinecone_index_namespace']
                                        ) 
                    response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
                st.session_state.requests.append(query)
                st.session_state.responses.append(response) 
        with response_container:
            if st.session_state['responses']:

                for i in range(len(st.session_state['responses'])):
                    message(st.session_state['responses'][i],key=str(i))
                    if i < len(st.session_state['requests']):
                        message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')
    except Exception as error_message:
        print(error_message)
        st.error("Error occured. Check your Credentials")