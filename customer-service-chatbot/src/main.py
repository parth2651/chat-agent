import streamlit as st
import bedrockclient as bedrockclient
from datetime import datetime
import utils as utils
import json

st.title("Semtech customer service chatbot")

agent_id ='0JUQ7PSUXX'
agent_alias_id='QZBAYQA2X1'
if "session_id" not in st.session_state:
    st.session_state.session_id = str(datetime.now()).replace(" ", "_")

# Function to parse and format response
def get_response(user_input):
    print(f"session id: {st.session_state.session_id}")
    response, trace, citations = bedrockclient.invoke_agent(user_input, agent_id, agent_alias_id, st.session_state.session_id)
    print(f"response from bedrock agent: {response}")
    return response, trace, citations
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        for content in message['content']:
            st.markdown(content['text'])

# Accept user input
if prompt := st.chat_input("How can i help you today?"):
    message = {"role":"user", "content": [{"text" : prompt}]}
    # Add user message to chat history
    st.session_state.messages.append(message)
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = bedrockclient.generate_conversation(prompt, st.session_state.messages, st.session_state.session_id)
        output_message = response['output']['message']

        # Show the complete conversation.
        for content in output_message['content']:
            if 'text' in content:
                st.markdown(content['text'])
                content_asst = {"role":"assistant", "content": [{"text" : content['text']}]}
                st.session_state.messages.append(content_asst)

# Display a button to end the session
end_session_button = st.button("End Session", on_click=utils.clear_input)

if end_session_button:
    st.markdown("Thank you for contacting customer support. Have a great rest of your day!")