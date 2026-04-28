import botocore.exceptions
def clear_guardrail (bedrock_client, guardrail_id):
    try:
        # Clean up - delete the guardrail
        bedrock_client.delete_guardrail(guardrailIdentifier=guardrail_id)
        print(f"Successfully deleted guardrail: {guardrail_id}")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Guardrail {guardrail_id} does not exist or was already deleted.")
        else:
            print(f"An error occurred: {e.response['Error']['Code']}")
            print(f"Error message: {e.response['Error']['Message']}")
            raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise
