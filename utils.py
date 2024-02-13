from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from sentence_transformers import SentenceTransformer
import pinecone 
from langchain.vectorstores import Pinecone
from langchain.document_loaders import PyPDFLoader
import tempfile
import streamlit as st
import openai

# To create embeddings on hard disk
@st.cache_resource(allow_output_mutation=True)
def get_embeddings_model():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return model, embeddings

model, embeddings = get_embeddings_model()

def ingest(
        uploaded_document, 
        pinecone_api_key, 
        pinecone_env, 
        pinecone_index_namespace, 
        chunk_size=500,
        chunk_overlap=20
        ):
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(uploaded_document.getbuffer())
        file_path = tf.name
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    # embeddings = get_embeddings_model()
    pinecone.init(
        api_key=pinecone_api_key,
        environment=pinecone_env
    )
    index_name = pinecone_index_namespace
    try:
        index = Pinecone.from_documents(docs, embeddings, index_name=index_name)
        st.success('Document uploaded to Pinecone database successfully')
    except Exception as error_message:
        st.error(error_message)

# # To create embeddings on hard disk
# # !pip install chromadb
# # from langchain.vectorstores import Chroma
# # persist_directory = './data/embeddings'
# # vStore = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)


def query_refiner(conversation, query):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response['choices'][0]['text']


def find_match(input, pinecone_api_key, pinecone_env, pinecone_index_namespace):
    pinecone.init(
        api_key=pinecone_api_key,
        environment=pinecone_env
    )
    index = pinecone.Index(pinecone_index_namespace)
    input_em = model.encode(input).tolist()
    result = index.query(input_em, top_k=2, includeMetadata=True)
    return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']


def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):        
        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
    return conversation_string
