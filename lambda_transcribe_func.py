import json
import boto3
import uuid
import os

# Initialize Boto3 client
s3_client = boto3.client('s3')
transcribe_client = boto3.client('transcribe')

def lambda_handler(event, context):
    
    sourcebucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    destbucket = 'audiotranscribebucketllm'


    try:
        
        job_name = 'transcription-job-' + str(uuid.uuid4()) # Needs to be a unique name

        response = transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': f's3://{sourcebucket}/{key}'},
            MediaFormat='mp3',
            LanguageCode='en-US',
            OutputBucketName= destbucket,  # specify the output bucket
            OutputKey=f'{job_name}-transcript.json',
            Settings={
                'ShowSpeakerLabels': True,
                'MaxSpeakerLabels': 5
            }
        )
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error occurred: {e}")
        }

    return {
        'statusCode': 200,
        'body': json.dumps(f"Submitted transcription job for {key} from bucket {sourcebucket}.")
    }