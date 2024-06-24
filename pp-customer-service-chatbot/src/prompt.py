def prepare_orchestration_systemprompt():
  prompt = """You are a customer support chatbot for Semtech.
  You will be acting as a semiconductor and product specialist created by company Semtech.
  you will be replying to users who asks questions related product information, troubleshooting products and training materials.
  you should maintain friendly customer service voice.
  """
  #print (prompt)
  return prompt
  
def prepare_orchestration(messages):
  prompt = f"""
  here is your previous conversastion {messages} 
  you job is to understand and identify if customer is looking to check warrenty or customer have problem with a product and what is the problem. you do not need to solve it.
  understand customer's question and ask clarifying qusestion in different way until you have information to troubleshoot.
  Here are some important rules for the interaction:
  <rules>
  - first Identify the problem is for warrenty check or product toubleshooting. 
  - If customer asks help about a product, ask for product name.
  - If you receive the product name, ask what specific problem the customer is facing.
  - If customer is looking to check warrenty asks for warrenty number.
  </rules>
  """
  prompt = prompt 
  return prompt
  
def prepare_validate_systemprompt():
  prompt = f"""You are a senior customer support executive Semtech. you job is to answer yes or no."""
  #print (prompt)
  return prompt

def prepare_validate_orchestration(messages):
  prompt = f"""
  here is your previous conversastion {messages} 
  based on the conversastion do you have enough information information of the problem and the product name user is facing issue with?
  Here are some important rules for the interaction
  <rules>
  - for product problem you need to have information about product name and information about the problem user is facing before saying yes.
  - for the warranty check you need to have warrenty number before saying yes.
  - answer should be only 'yes' or 'no' without any other details.
  </rules>
  """
  return  prompt

def prepare_extract_systemprompt():
  prompt = f"""You are a senior customer support executive Semtech. """
  #print (prompt)
  return prompt

def prepare_extract_details(messages):
  prompt = f"""
    here is your previous conversastion {messages}
    you job is to understand and identify if customer is looking to check warrenty or customer have problem with a product and what is the problem. you do not need to solve it.
    based on the conversastion find the product name, problem with the product and warranty as shown in the <example> tag
    Here are some important rules for the interaction
    <rules>
    - extract the details based on conversastion 
    - response should be as shown in example no extra words.
    </rules>
    <examples>
      <example>
        <product>NT24L71</product>
        <troubleshooting>pin is broken</troubleshooting>
        <warranty></warranty>
      </example>
      <example>
        <product>1.25Gbps CML Limiting Amplifier</product>
        <troubleshooting>device is not powring on</troubleshooting>
        <warranty></warranty>
      </example>
      <example>
        <product>Amplifier</product>
        <troubleshooting></troubleshooting>
        <warranty>892402834748392</warranty>
      </example>
      <example>
        <product></product>
        <troubleshooting></troubleshooting>
        <warranty>892412854747392</warranty>
      </example>
    </examples>
    """
#print (prompt)
  prompt = prompt 
  return prompt







# def prepare_orchestration(messages):
#   prompt = f"""
#   here is your previous conversastion {messages} 
#   you job is to understand and identify if customer is looking to check warrenty or customer have problem with a product and what is the problem. you do not need to solve it.
#   understand customer's question and ask clarifying qusestion in different way until you have information to troubleshoot.
  
#   only once you identify the request respond as shown in the <examples> tag
#   <rules>
#   - first Identify the problem is for warrenty check or product toubleshooting. 
#   - If customer asks help about a product, ask for product name.
#   - If you receive the product name, ask what specific problem the customer is facing.
#   - If customer is looking to check warrenty asks for warrenty number.
#   </rules>
#   <examples>
#     <example>
#       <product>NT24L71</product>
#       <troubleshooting>pin is broken</troubleshooting>
#       <warrenty></warrenty>
#     </example>
#     <example>
#       <product>1.25Gbps CML Limiting Amplifier</product>
#       <troubleshooting>device is not powring on</troubleshooting>
#       <warrenty></warrenty>
#     </example>
#     <example>
#       <product>Amplifier</product>
#       <troubleshooting></troubleshooting>
#       <warrenty>892402834748392</warrenty>
#     </example>
#   </examples>
  
#   """
#  - If you receive the product name and what is the problem users are facing. 
#  - user says what problem they are facing the products is not working or asks a troubleshooting question
#   prompt = prompt 
#   return prompt
  