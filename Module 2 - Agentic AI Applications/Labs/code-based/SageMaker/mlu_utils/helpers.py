import boto3
from botocore.exceptions import ClientError
import json
import random
import string

# Common inference parameters for Converse API
converse_inference_params = {
    "maxTokens": "(int) Maximum number of tokens to generate",
    "temperature": "(float) Temperature for sampling",
    "topP": "(float) Top P for nucleus sampling",
    "stopSequences": "([string]) Sequences that stop generation"
}

def validate_inference_parameters(inference_config):
    """Validates inference parameters for Converse API"""
    for key in inference_config:
        if key not in converse_inference_params:
            raise ValueError(f"'{key}' is not a valid inference parameter for Converse API")
    return True

def validate_model_access(model_id):
    """Validates access to requested model using Converse API.
    
    Return True when model is accessible and False otherwise
    """
    bedrock_runtime = boto3.client(service_name="bedrock-runtime")
    
    try:
        # Simple test request using Converse API format
        request = {
            "modelId": model_id,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": "How are you?"
                        }
                    ]
                }
            ],
            "inferenceConfig": {
                "maxTokens": 64,
                "temperature": 0.5
            }
        }
        
        bedrock_runtime.converse(**request)
        return True
    except ClientError as error:
        if error.response['Error']['Code'] == 'AccessDeniedException':
            return False
        else:
            return False

def validate_models_access(model_ids):
    """Validates access to list of model ids using Converse API.

    Returns an empty list if all models are accessible and a list of inaccessible models otherwise.
    """
    return [
    str(f"Congrats! You have access to {model_id} model")
    if validate_model_access(model_id)
    else str(f"Sorry, you don't have access to {model_id} model. Reach out to the account administrator to give you access")
    for model_id in model_ids
    ]



# for generating our mock AUTH KEYS
def generate_random_string(length=34):
    # Define the character set (letters and numbers)
    chars = string.ascii_letters + string.digits
    
    # Generate random string using random.choices
    random_string = ''.join(random.choices(chars, k=length))
    
    return str(random_string)

