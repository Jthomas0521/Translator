import os
import requests
import json

LIBRE_TRANSLATE_URL = os.environ.get("LIBRE_TRANSLATE_URL")
data = {'q': "Hello. My name is Jahquan", 'source': "en", 'target': "es", 'format': "text"}

response = requests.post(LIBRE_TRANSLATE_URL, data=data)

if response.status_code == 200:
    # print("Translation success: 200")
    # print(response.text)
    print(type(response.text))

    json_response = json.loads(response.text)
    print(type(json_response))
    print(json_response['translatedText'])


else:
    print(f"Translation error: {response.status_code}")
