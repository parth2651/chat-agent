# agent-chatbot



## Getting started
This repo assumes you have infrastructure setup in place which includes 
1. Setting up Bedrock model access
2. Creating knowledgebase 
3. Creating Agent

This also assumes that you have AWS access setup from where you are running the streamlit application.

Changes to the above coming soon.

### Create a python virtual environment and initialize it
```
python3 -m venv .venv
source .venv/bin/activate
```

### Install the necessary libraries
```
pip install -r requirements.txt
```

### Run streamlit app, pass agent_id and agent_alias_id as command line args
```
streamlit run src/main.py -- --agent_id=123456 --agent_alias_id=123456
```

