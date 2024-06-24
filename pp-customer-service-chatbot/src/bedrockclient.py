import boto3
import json
from botocore.exceptions import ClientError
import logging
import os
from llmcall import * 
from prompt import *

#bedrock_config = Config(connect_timeout=120, read_timeout=120, retries={'max_attempts': 0})
#bedrock_agent_client = boto3.client("bedrock-agent-runtime",config=bedrock_config)
bedrock_agent_client = boto3.client("bedrock-agent-runtime")
bedrock_client = boto3.client("bedrock-runtime")
bedrock_runtime = boto3.client('bedrock-runtime')
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

KB_ID = '1KBBDFUTW4'

tool_list = [
    {
        "toolSpec": {
            "name": "knowledgebase",
            "description": "Call knowledgebase for product information, training material, and troubleshooting guide.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "productName": {
                            "type": "string",
                            "description": "Product Name"
                        }
                    },
                    "required": ["productName"]
                }
            }
        }
    },
    {
        "toolSpec": {
            "name": "warrntycheck",
            "description": "Tool to check warranty info",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "serialNumber": {
                            "type": "number",
                            "description": "The serial number to pass to the function."
                        }
                    },
                    "required": ["serialNumber"]
                }
            }
        }
    }
]

def orchestrate_conversation(prompt, messages, session_id):
   print(f"""**** Messages ***** {messages}""")
   model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
   if 'yes' in validate_orchestration(messages):
       details = extract_details(messages)
       print("deails")
       print(details)
       response  = details
   else:
       systempromptAI = prepare_orchestration_systemprompt()
       prompt = prepare_orchestration(messages)
       answer = interactWithLLMTextfromAnthropic(bedrock_runtime,prompt,'',model_id,systempromptAI)
       response  = answer
       print("checking response:" + response)
   return response 

def validate_orchestration(messages):
   model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
   systempromptAI = prepare_validate_systemprompt()
   prompt = prepare_validate_orchestration(messages)
   answer = interactWithLLMTextfromAnthropic(bedrock_runtime,prompt,'',model_id,systempromptAI)
   print("can answer?:"+ answer.lower())
   return answer.lower()

def extract_details(messages):
   model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
   systempromptAI = prepare_extract_systemprompt()
   prompt = prepare_extract_details(messages)
   answer = interactWithLLMTextfromAnthropic(bedrock_runtime,prompt,'',model_id,systempromptAI)
   print("details: "+answer)
   return answer 

def generate_conversation(messages):

    print("**** Messages ***** {messages}")
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    # system_prompt = [{"text": "You are a customer support chatbot for Semtech. "
    #               "Customer will ask questions on product information, troubleshooting products and ask for training materials"
    #               "Be respectiful and direct. Ask clarifying questions if customer doesnt provide specific prodict model name."}]
    
    system_prompt = [{"text": "You are a customer support chatbot for Semtech. "
            "Customer will ask questions on product information, troubleshooting products and training materials. Ask for clarifying questions." 
            "- If customer asks help about a product, ask for product name."
            "- If you receive the product name, ask what specific problem the customer is facing."
            "- If you receive the product name and user says the products is not working or asks a troubleshooting question, only then invoke the knowledgebase tool."
            "- If user asks about warranty and you have the serial number, only then invoke warrantyCheck tool"}]
    print(messages)
    # Inference parameters to use.
    temperature = 0.5
    top_k = 200

    # Base inference parameters to use.
    inference_config = {"temperature": temperature}

    # Additional inference parameters to use.
    additional_model_fields = {"top_k": top_k}

    response = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        system=system_prompt,
        inferenceConfig=inference_config,
        additionalModelRequestFields=additional_model_fields,
        toolConfig={"tools":tool_list}
    )
            
    # Log token usage.
    token_usage = response['usage']
    logger.info("Input tokens: %s", token_usage['inputTokens'])
    logger.info("Output tokens: %s", token_usage['outputTokens'])
    logger.info("Total tokens: %s", token_usage['totalTokens'])
    logger.info("Stop reason: %s", response['stopReason'])

    print("**** LLM response start*****")
    print(response)
    print("**** LLM response end *****")

    response_content_blocks = response['output']['message']['content']

    print(f'** Prompt*** {prompt}')
    for content_block in response_content_blocks:
        if 'toolUse' in content_block:
            tool_use_block = content_block['toolUse']
            tool_use_name = tool_use_block['name']
            
            print(f"Using tool {tool_use_name}")
            
            if tool_use_name == 'warrantycheck':
                print("warranty check")
            elif tool_use_name == 'knowledgebase':
                kb_response = retrievefromKB(messages, session_id, tool_use_block['input']['productName'])
                response = {"output": {"message" : {"role": "assistant", "content" : [{"text": kb_response['output']['text']}]}}}
                
        elif 'text' in content_block:
            print(content_block['text'])

    return response

def retrievefromKB(messages, session_id, product_name) :
    region = 'us-west-2'
    model_arn = f'arn:aws:bedrock:{region}::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'

    prompt = ''
    for message in messages:
        if message['role'] == 'user':
            for content in message['content']:
                if 'text' in content:
                    prompt += content['text']
    print("*****KB Prompt start*****")
    print(prompt)
    print("*****KB Prompt end*****")
    response = ''
    response = bedrock_agent_client.retrieve_and_generate(
        input={
            'text': prompt
        },
        retrieveAndGenerateConfiguration={
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': KB_ID,
                'modelArn': model_arn,
                'retrievalConfiguration' : {
                    'vectorSearchConfiguration' : {
                        'filter' : {
                            'stringContains' : {
                                'key' : 'productName',
                                'value' : product_name
                            }
                        }
                    }
                }
            }
        }
        #sessionId=session_id
        )
    print(response)
    citations = response["citations"]
    contexts = []
    for citation in citations:
        retrievedReferences = citation["retrievedReferences"]
        for citation in citations:
            retrievedReferences = citation["retrievedReferences"]
            for reference in retrievedReferences:
                contexts.append(reference["location"]["s3Location"]["uri"])
    print(contexts)
    return response



def orchestrator(messages) :
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    system_prompt = '''You are an orchestrator for the flow of logic. If the prompt has warranty in it, suggest "Invoke Warranty function". 
                        If prompt asks about any other info, suggest "Invoke knowledge base". Please your suggestion in "nextpath" XML tag'''
    
    native_request = {
        "system": system_prompt,
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.5,
        "messages": messages,
    }
    request = json.dumps(native_request)
    
    try:
        response = bedrock_client.invoke_model(modelId=model_id,body=request)
        # Decode the response body.
        model_response = json.loads(response["body"].read())
        # Extract and print the response text.
        response_text = model_response["content"][0]["text"]
        print(response_text)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")

if __name__ == '__main__':
    messages = [{"role": "user", "content": [{"text":"Need help with a product Airlink 90 and serial number 123456"}]}]
    generate_conversation(messages)

    # messages = [{"role": "user", "content": [{"type":"text","text":"Need help with wrranty"}]}]
    # orchestrator(messages)

    # print(response)

