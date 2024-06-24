import boto3

boto3_session = boto3.session.Session()
client = boto3_session.client("bedrock-agent")

response = client.start_ingestion_job(
    knowledgeBaseId = 'XJ9GEZ9D5T', 
    dataSourceId = '3I9FTRWPOV'
)

