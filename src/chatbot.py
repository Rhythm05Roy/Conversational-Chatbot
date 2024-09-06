import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

load_dotenv()

def create_conversation_Chain():
    llm = ChatGroq(
        model="llama-3.1-70b-versatile",
        temperature=0.2
    )

    memory = ConversationBufferMemory()
    chain = ConversationChain(
        llm=llm,
        memory=memory,
        verbose =True
    )
    return chain

st.set_page_config(
    page_title="Conversational Bot",
    page_icon="🤖",
    layout='centered'
    )

st.title('🤖Conversational Bot')

if "conversation_chain" not in st.session_state:
    st.session_state.conversation_chain = create_conversation_Chain()

if "chat_history" not in st.session_state:
    st.session_state.chat_history =[]

for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_input = st.chat_input('Ask your question:')

if user_input:
    st.session_state.chat_history.append({"role":"user", "content":user_input})

    with st.chat_message('user'):
        st.markdown(user_input)

    response = st.session_state.conversation_chain.run(input = user_input)

    st.session_state.chat_history.append({"role":"assistant", "content":response})

    with st.chat_message('assistant'):
        st.markdown(response)

if st.button('Clear chat history'):
    st.session_state.chat_history = []
    st.session_state.conversation_chain = create_conversation_Chain()
    st.experimental_rerun()