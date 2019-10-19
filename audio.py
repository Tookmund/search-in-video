import time
import requests
from collections import OrderedDict
import boto3
import os

import s3

def aud2text(filename, h):
    transcribe = boto3.client('transcribe')
    s3.uploadfile(filename, f"pending-{h}.wav")
    job_name = h+os.urandom(16).hex()
    job_uri = f"https://s3.us-east-1.amazonaws.com/search-in-video/pending-{h}.wav"
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='wav',
        LanguageCode='en-US'
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Audio not ready yet...")
        time.sleep(5)
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        r = requests.get(status['TranscriptionJob']['Transcript']['TranscriptFileUri'])
        return json.loads(r.text())
    return {}
