import boto3

client = boto3.client("bedrock-agent-runtime")


def invoke_agent(prompt, agent_id, alias_id, session_id):
    response = client.invoke_agent(inputText=prompt,
        agentId=agent_id,
        agentAliasId=alias_id,
        sessionId=session_id,
        enableTrace=True
    )

    completion = ''
    contexts = []
    trace = []
    try:
        for event in response.get("completion"):
            print(f"Event********.. {event}")
            if 'chunk' in event:
                #print(event['chunk'])
                chunk = event['chunk']
                completion = completion + chunk['bytes'].decode('utf8')

                if 'attribution' in chunk:
                    citations = chunk['attribution']['citations']
                    for citation in citations:
                        retrievedReferences = citation["retrievedReferences"]
                        for reference in retrievedReferences:
                            contexts.append(reference["location"]["s3Location"]["uri"])
            elif 'trace' in event:
                trace.append(event['trace'])
            else:
                raise Exception("unexpected event.", event)
    except Exception as e:
        raise Exception("unexpected event.", e)

    return completion, trace, contexts


