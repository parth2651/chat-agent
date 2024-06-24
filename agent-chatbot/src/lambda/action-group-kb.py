
import json

import sys
from pip._internal import main

main(['install', '-I', '-q', 'boto3', '--target', '/tmp/', '--no-cache-dir', '--disable-pip-version-check'])
sys.path.insert(0,'/tmp/')
import boto3

bedrock_agent_client = boto3.client("bedrock-agent-runtime")
KB_ID = '1KBBDFUTW4'

def get_named_parameter(event, name):
    return next(item for item in event['parameters'] if item['name'] == name)['value']

def lambda_handler(event, context):
    print('boto3 version => ' +boto3.__version__)
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])
    inputText = event['inputText']
    session_id = event['sessionId']
    
    product_name = get_named_parameter(event, "product_name")
    prompt = get_named_parameter(event, "prompt")
    
    
    region = 'us-west-2'
    model_arn = f'arn:aws:bedrock:{region}::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0'

    #prompt = inputText + " " + product_name
    print(f"Input text----- {inputText}")
    print(f"*****Input prompt----- {prompt}")
    #print(f"Prompt----- {prompt}")
    print(f"Product name -----{product_name}")

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
                # 'retrievalConfiguration' : {
                #     'vectorSearchConfiguration' : {
                #         'filter' : {
                #             'stringContains' : {
                #                 'key' : 'productName',
                #                 'value' : product_name
                #             }
                #         }
                #     }
                # }
            }
        },
        #sessionId=session_id
        )
    print(response)
    
    citations = response["citations"]
    contexts = []
    referencestring= ""
   
    for citation in citations:
        retrievedReferences = citation["retrievedReferences"]
        for citation in citations:
            retrievedReferences = citation["retrievedReferences"]
            for reference in retrievedReferences:
                allmetadata = reference["metadata"]
                for metadata in allmetadata:
                    if 'SourceURL' in metadata:
                        contexts.append(reference["metadata"][metadata])
    referencestring = join_elements(set(contexts),', ')
                    
    print("***referencestring***" + referencestring)
    #response = response['output']['text']
    if referencestring == "":
        response = response['output']['text']
    else:
        response = response['output']['text'] + " To get more details please refer to the source URL:"+ referencestring
    print(response)
    responseBody =  {
        "TEXT": {
            "body": response
        }
    }

    action_response = {
        'actionGroup': actionGroup,
        'function': function,
        'functionResponse': {
            'responseBody': responseBody
        }

    }

    function_response = {'response': action_response, 'messageVersion': event['messageVersion']}
    print("Response: {}".format(function_response))

    return function_response


def join_elements(set_obj, sep=', '):
    joined_str = ''
    i = 0
    for el in set_obj:
        joined_str += el
        if i < len(set_obj) - 1:
            joined_str += sep
        i += 1
    return joined_str
