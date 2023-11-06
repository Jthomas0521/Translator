import os
import requests


LIBRE_TRANSLATE_URL = os.environ.get("LIBRE_TRANSLATE_URL")
data = {'input_text': 'Your test text here'}

response = requests.post(LIBRE_TRANSLATE_URL, data=data)

if response.status_code == 200:
    print("Translation success:")
    print(response.text)
else:
    print(f"Translation error: {response.status_code}")
