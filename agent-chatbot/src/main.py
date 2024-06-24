import streamlit as st
import invokeagent as agent
from datetime import datetime
import utils as utils
import argparse

st.title("Customer service chatbot")

parser = argparse.ArgumentParser()
parser.add_argument("--agent_id", type=str, default="default")
parser.add_argument("--agent_alias_id", type=str, default="default")
args = parser.parse_args()

agent_id = args.agent_id
agent_alias_id=args.agent_alias_id

if "session_id" not in st.session_state:
    st.session_state.session_id = str(datetime.now()).replace(" ", "_")

# Function to parse and format response
def get_response(user_input):
    print(f"session id: {st.session_state.session_id}")
    response, trace, citations = agent.invoke_agent(user_input, agent_id, agent_alias_id, st.session_state.session_id)
    print(f"response from bedrock agent: {response}")
    return response, trace, citations
    
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can i help you today?"):
    # Add user message to chat history
    content = [{"text": prompt}]
    st.session_state.messages.append({"role": "user", "content": content})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

# Display assistant response in chat message container
    with st.chat_message("assistant"):
        response, trace, citations = get_response(prompt)
        st.markdown(response)
        if citations:
            st.markdown(citations)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display a button to end the session
end_session_button = st.button("End Session", on_click=utils.clear_input)

if end_session_button:
    st.markdown("Thank you for contacting customer support. Have a great rest of your day!")