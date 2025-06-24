
import os
import streamlit as st
from Agent import graph




st.title ("Autonomous Multi-Agent Podcast Generator")
#background-color: #f1f0f0; #dcf8c6;

st.markdown("""
    <style>
    .chat-bubble {
        
        max-width: 90%;
        padding: 10px;
        border-radius: 15px;
        margin: 10px;
        word-wrap: break-word;
        font-size: 20px;
    }
    .user-bubble {
        background-color: #f1f0f0;
        margin-left: auto;
        
        position: relative;
    }
    .user-bubble::before {
        content: "💬";
        position: absolute;
        top: -20px;
        right: 0;
        font-size: 26px;
        text-align: right;
    }
    .assistant-bubble {
        
        margin-right: auto;
        text-align: left;
        position: relative;
    }
    .assistant-bubble::before {
        content: "🧠";
        position: absolute;
        top: -20px;
        left: 0;
        font-size: 26px;
    }
    textarea {
        font-size: 18px !important;
        padding: 10px !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)




if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message['role'] == 'user':
        #m = st.chat_message('user')
        st.markdown (f'<div class="chat-bubble user-bubble"> {message["content"]}</div>', unsafe_allow_html=True)
    else:
        #m = st.chat_message('assistant')
        st.markdown(f'<div class="chat-bubble assistant-bubble"> {message["content"]}</div>', unsafe_allow_html=True)

thread = {'configurable': {'thread_id': "10"}}
if 'podcastGraph' not in st.session_state:
    st.session_state.podcastGraph = graph.graph()

podcastGraph = st.session_state.podcastGraph

if prompt := st.chat_input ("Podcast Description"):
    #m = st.chat_message('human')
    st.markdown (f'<div class="chat-bubble user-bubble">  {prompt}</div>', unsafe_allow_html=True)
    #m.markdown (prompt)
        
    st.session_state.messages.append ({'role': 'user', 'content': prompt})

    with st.spinner ("Generating Podcast Details"):
        if podcastGraph.get_state (thread).next:
            msg = prompt
            podcastGraph.update_state (config=thread,
                                           values={'humanFeedback': msg},
                                           as_node='human feedback')
            
            for event in podcastGraph.stream (None, config=thread,
                                                  stream_mode='values'):
                pass

        else:
            msg = prompt
            for event in podcastGraph.stream ({'message': msg, 'feedback': False},
                                                  config=thread,
                                                  stream_mode='values'):
                pass


    if podcastGraph.get_state (thread).next:  
        values = podcastGraph.get_state(thread).values
        podcastDetail = values['podcastDetail']
        focusPoint = "\n\n".join (values.get ('focusPoints', []))

        tt = f"""

**Generated Podcast Detaild**

**Podcast Topic:** {podcastDetail.topic}.
\n**Podcast Discusion Area:** {podcastDetail.discusionArea}.
\nInterviewer is {podcastDetail.interviewerName} a {podcastDetail.interviewer}
\nExpert is {podcastDetail.expertName} a {podcastDetail.expert}

**Podcast Focus Points:**\n
{focusPoint}
"""
                    
        
        #m = st.chat_message ('assistant')
        st.markdown(f'<div class="chat-bubble assistant-bubble">  {tt}</div>', unsafe_allow_html=True)
        #m.markdown(result)

        st.session_state.messages.append ({'role': 'assistant', 'content': tt})

    else:
        fileName = podcastGraph.get_state (thread).values['fileName']
        with open (fileName, "rb") as f:
            audio = f.read()
        
        st.audio (audio, format="audio/mp3")
        del st.session_state['podcastGraph']
    


