import boto3
import json
from .config_loader import config

bedrock = boto3.client('bedrock-runtime', region_name=config["aws_region"])

def get_embedding(text):
    payload = { "inputText": text }
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=json.dumps(payload),
        accept="application/json",
        contentType="application/json"
    )
    return json.loads(response['body'].read())['embedding']

def get_llm_response(prompt):
    payload = {
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7,
        "stop_sequences": ["\n"]
    }
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(payload),
        accept="application/json",
        contentType="application/json"
    )
    return json.loads(response['body'].read())['completion']
