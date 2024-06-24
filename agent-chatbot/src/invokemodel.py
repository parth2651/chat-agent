import boto3
import logging

bedrock_client = boto3.client("bedrock-runtime")

model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def generate_conversation(messages):

    # system_prompt = [{"text": "You are a customer support chatbot for Semtech. "
    #               "Customer will ask questions on product information, troubleshooting products and ask for training materials"
    #               "Be respectiful and direct. Ask clarifying questions if customer doesnt provide specific prodict model name."}]
    
    system_prompt = [{"text": "You are a customer support chatbot for Semtech. "
            "Customer will ask questions on product information, troubleshooting products and ask for training materials"
            "Be respectiful and direct. Ask for model name and serial number."
            "Place the model name and serial number that customer provides in 'parameters' XML tags when you receive them from customer."}]
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
        additionalModelRequestFields=additional_model_fields
    )
            
    # Log token usage.
    token_usage = response['usage']
    logger.info("Input tokens: %s", token_usage['inputTokens'])
    logger.info("Output tokens: %s", token_usage['outputTokens'])
    logger.info("Total tokens: %s", token_usage['totalTokens'])
    logger.info("Stop reason: %s", response['stopReason'])

    return response
    
    def decompose_prompts() :
        system_prompt = [{"text": "You are a customer support chatbot for Semtech. "
                  "Customer will ask questions on product information, troubleshooting products and ask for training materials"
                  "Be respectiful and direct. Ask for model name and serial number."
                  "Place the model name that customer gives in 'model' XML tags."
                  "Place the serial number that customer gives in 'serialnumber' XML tags"}]
        
        
    