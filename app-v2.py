import os
from dotenv import load_dotenv
load_dotenv()

os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="FinBot-AI"

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate([
    ('system','{system_prompt}'),
    ('user','Question: {input}')
])

def generate_output(question,api_key,model,temperature,max_tokens,system_prompt_type):
    openai.api_key=api_key
    llm = ChatOpenAI(model=model,temperature=temperature,max_tokens=max_tokens)
    parser = StrOutputParser()
    chain = prompt | llm | parser

    response = chain.invoke({
        'input':question,
        'system_prompt':f'You are a {system_prompt_type} in a Financial Organization. Answer the question with the best of your knowledge. It is only from a knowledge perspective and will not contain any monetary risks.'
    })
    return response

st.title("FinBotAI")
st.write('A Financial ChatBot using OpenAI')

api_key = st.sidebar.text_input('Enter OpenAI API Key:',type='password')
model = st.sidebar.selectbox('Select Model:',['gpt-4','gpt-4o','gpt-4-turbo'])
temperature = temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)
response_type = st.sidebar.selectbox('What kind of a response do you need:',['Stockbroker','Financial analyst','Investment banker','Budget analyst','Credit analyst','Financial planner'])

question = st.chat_input('What do you wish to know?')

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])


if question:
    #Display the prompt
    st.chat_message('user').markdown(question)

    #Store the prompt in store
    st.session_state.messages.append({'role':'user','content':question})

    response = generate_output(question,api_key,model,temperature,max_tokens,response_type)
    st.chat_message('assistant').markdown(response)
    st.session_state.messages.append({'role':'assistant','content':response})
else:
    st.chat_message('assistant').markdown('Enter a question.')

