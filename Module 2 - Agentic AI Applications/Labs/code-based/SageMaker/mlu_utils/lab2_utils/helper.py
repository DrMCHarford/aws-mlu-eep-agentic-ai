import os
import boto3
import re
from botocore.exceptions import ClientError
from strands.models import BedrockModel
from botocore.config import Config as BotocoreConfig

def get_bedrock_model(model_id="amazon.nova-pro-v1:0"):
    boto_config = BotocoreConfig(
        retries={"max_attempts": 3, "mode": "standard"},
        connect_timeout=5,
        read_timeout=60
    )
    
    # Create a configured Bedrock model
    bedrock_model = BedrockModel(
        model_id=model_id,
        boto_client_config=boto_config,
    )
    return bedrock_model

# Function to extract Task ARN and derive S3 location
def extract_task_info_and_s3_location(response_text, s3_bucket):
    # Look for Task ARN pattern in the response
    task_arn_pattern = r'arn:aws:bedrock:[^:]+:[^:]+:async-invoke/([a-zA-Z0-9]+)'
    match = re.search(task_arn_pattern, response_text)
    
    if match:
        task_id = match.group(1)
        # Construct S3 location based on the pattern: <S3_BUCKET>/<task_id>/output.mp4
        object_key = f"{task_id}/output.mp4"
        s3_uri = f"s3://{s3_bucket}/{object_key}"
        return task_id, s3_uri, object_key
    return None, None, None

# Function to check if video generation is complete by trying to access the file
def check_video_availability(s3_client, bucket_name, object_key):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=object_key)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise e

def retrieve_generated_video(video_generation_response, s3_bucket): 
    # Try to extract Task ARN and derive S3 location from the agent's response
    try:
        if 'content' in video_generation_response.message and isinstance(video_generation_response.message['content'], list):
            response_text = video_generation_response.message['content'][0]['text']
        else:
            response_text = str(video_generation_response.message)
        
        task_id, s3_uri, object_key = extract_task_info_and_s3_location(response_text, s3_bucket)
        
        if task_id and s3_uri:
            print(f"🔍 Found Task ID: {task_id}")
            print(f"🔍 Derived S3 URI: {s3_uri}")
            
            # Setup download path
            download_dir = "downloaded_videos"
            os.makedirs(download_dir, exist_ok=True)
            
            # Create filename with task ID
            filename = f"video.mp4"
            download_path = os.path.join(download_dir, filename)
            
            try:
                # Initialize S3 client
                s3_client = boto3.client('s3', region_name="us-east-1")
                
                print(f"⏳ Checking if video is ready at {s3_bucket}/{object_key}...")
                
                # Check if video is available
                if check_video_availability(s3_client, s3_bucket, object_key):
                    print(f"✅ Video found! Downloading...")
                    s3_client.download_file(s3_bucket, object_key, download_path)
                    
                    # Get file size for confirmation
                    file_size = os.path.getsize(download_path)
                    print(f"✅ Video successfully downloaded to: {download_path}")
                    print(f"   File size: {file_size:,} bytes")
                    print(f"   You can view the video using a media player of your choice.")
                    return download_path
                    
                else:
                    print("⏳ Video generation is still in progress...")
                    print("\n👤 Message to user:")
                    print("   The video generation process is still running.")
                    print("   Video generation typically takes 5-10 minutes.")
                    print(f"   Task ID: {task_id}")
                    print(f"   Expected S3 location: {s3_uri}")
                    print("   Please try downloading the video again in a few minutes.")
                    
            except ClientError as e:
                error_code = e.response['Error']['Code']
                if error_code == 'NoSuchKey':
                    print("⏳ Video not yet available in S3...")
                    print("\n👤 Message to user:")
                    print("   The video generation process may still be in progress.")
                    print("   Please try downloading the video again in a few minutes.")
                    print(f"   Expected S3 location: {s3_uri}")
                elif error_code == 'AccessDenied':
                    print("❌ Access denied to S3 bucket/object.")
                    print("   Please check your AWS credentials and S3 permissions.")
                else:
                    print(f"❌ Error accessing S3: {e}")
                    
        else:
            print("❌ Could not find Task ARN in the agent's response.")
            print("🔍 Response content:")
            print(f"   {response_text[:200]}...")
            print("\n👤 Message to user:")
            print("   Could not extract task information from the response.")
            print("   Please try generating the video again.")
            
    except Exception as e:
        print(f"❌ Error processing response: {e}")
        print("\n👤 Message to user:")
        print("   An error occurred while trying to process the video information.")
        print("   Please try generating the video again later.")

    return None