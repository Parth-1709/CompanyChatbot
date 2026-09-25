import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from sqlalchemy import create_engine
import sqlite3
from pathlib import Path
from langchain_community.utilities import SQLDatabase
from langchain.agents.middleware import SummarizationMiddleware
import uuid
from langchain.tools import tool

def get_retriever():
    loader = PyPDFLoader('JD_BTSA_2026.pdf')
    docs = loader.load_and_split(RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=50))
    embedding = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    db = FAISS.from_documents(docs,embedding)
    retriever =  db.as_retriever()
    return retriever

st.title('Company and Employee Info Assistant')
st.subheader('Tells you information about the database and Employee Policies :) ')

api_key = st.sidebar.text_input(label='Enter Groq API key',type='password')


if 'thread' not in st.session_state:
    st.session_state.thread=str(uuid.uuid4())

if 'retriever' not in st.session_state:
    retriever = get_retriever()
    st.session_state.retriever = retriever

if 'checkpoint' not in st.session_state:
    st.session_state.checkpoint = InMemorySaver()

if 'chats' not in st.session_state or st.sidebar.button('New Chat'):
    st.session_state.chats = [{'role':'assistant','content':'How can i help you'}]

for msg in st.session_state.chats:
    st.chat_message(msg['role']).write(msg['content'])

if api_key.strip():
    try:
        llm = ChatGroq(model='openai/gpt-oss-120b',api_key=api_key)
        def get_db():
                db_path = Path(__file__).parent/'employee.db'
                creator = lambda:sqlite3.connect(f'file:{db_path}?mode=ro',uri=True)
                return SQLDatabase(create_engine(f'sqlite:///',creator=creator))
        
        db = get_db()
        toolkit = SQLDatabaseToolkit(db=db,llm=llm)

        retriever = st.session_state.retriever

        @tool
        def doc_tool(input:str):
                '''Provide information about company policies and hiring.'''
                if retriever is None: return 'No document present'
                document = retriever.invoke(input)
                context = '\n\n'.join(doc.page_content for doc in document)
                return context
        
        tools = toolkit.get_tools()+[doc_tool]
        
        system_prompt = '''
                You are a helpful assistant . Use the required tools to answer questions about the company 
                as well as the employees working in it . And only answer question related to it if you don't find
                any context in the doc_tool or no entries in the database just return that you don't have the answer or 
                the question is invalid . Try to answer in minimal sentences if possible
            '''
        
        agent = create_agent(
                model=llm,
                checkpointer=st.session_state.checkpoint,
                system_prompt=system_prompt,
                tools=tools,
                middleware=[SummarizationMiddleware(
                    model=llm,
                    keep=('messages',4),
                    trigger=('messages',10)
                )]
            )
    except Exception as e:
        st.error(f'Error:{e}')
    
    



question = st.text_input(label=None,placeholder='Ask any question')

if st.button('Ask'):
    if not api_key and not question.strip():
        st.warning('Please provide the required information')
    else:
        streamlitcb = StreamlitCallbackHandler(st.container())
        config = {'configurable':{'thread_id':st.session_state.thread},'callbacks':[streamlitcb]}
        st.session_state.chats.append({'role':'user','content':question})
        st.chat_message('user').write(question)

        with st.chat_message('assistant'):
            result = agent.invoke({'messages':{'role':'user','content':question}},config=config)
            response = result['messages'][-1].content
            st.session_state.chats.append({'role':'assistant','content':response})
            st.write(response)




        



