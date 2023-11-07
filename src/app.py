import os
from flask import Flask, request, render_template, Response, jsonify
import requests
import logging
from dotenv import load_dotenv
import json

load_dotenv()

logger = logging.getLogger()

logger.setLevel(os.environ.get("LOG_LEVEL"))
app = Flask(__name__)


# Requests the current directory
APP_DIRECTORY = os.environ.get("APP_DIRECTORY")
logging.info(f'APP_DIRECTORY is {APP_DIRECTORY}')
profanity_words = os.path.join(APP_DIRECTORY, 'badwords.txt')

LIBRE_TRANSLATE_PORT = os.environ.get("LIBRE_TRANSLATE_PORT")


# Directory paths for input and output volumes
input_directory = os.path.join(APP_DIRECTORY, 'input')
output_directory = os.path.join(APP_DIRECTORY, 'output')

# Input and Output Directories
os.makedirs(input_directory, exist_ok=True)
os.makedirs(output_directory, exist_ok=True)

# Logging Info
# logging.basicConfig(filemode='w', level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
# string_handler = logging.StreamHandler()
# logger.addHandler(string_handler)


# Profanity Words Checker
def profanity(text):
    with open(profanity_words, 'r') as file:
        badwords = set(word.lower().strip() for word in file)

        # Splits the text
        split_text = text.lower().split()

        # Detects if any words  from the text are identified in the badwords.txt file
        for word in badwords:
            if word in split_text:
                logger.info(f"{word} is not allowed.")
                return True
        return False


# Translated Text
def text_translator(text) -> Response:
    LIBRE_TRANSLATE_URL = os.environ.get("LIBRE_TRANSLATE_URL")
    data = {'q': text, 'source': "auto", 'target': "es"}
    gen_response = requests.post(LIBRE_TRANSLATE_URL, data=data)

    logger.info(f"Translation Status Code: {gen_response.status_code}")
    logger.info(f"Translation Response Text: {gen_response.text}")

    if gen_response.status_code == 200:
        return gen_response.text
    else:
        return f"Translation error: {gen_response.status_code}"


# Translated text file
def file_translator(file_path):
    with open(file_path, 'r') as file:
        input_text = file.read()
        file_response = text_translator(input_text)

        # Checks to see if file_response produces an instance
        if isinstance(file_response, Response):
            return file_response.text

        else:
            return file_response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    input_text = request.form.get('input_text')
    file_path = request.form.get('file_path')

    if profanity(input_text):
        return "Profanity Detected. Please Remove."

    if file_path:
        file_path = os.path.join(APP_DIRECTORY, file_path)

        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                translated_text = file_translator(file_path)
            elif os.path.isdir(file_path):
                translated_text = ""

                for root, files in os.walk(file_path):
                    for filename in files:
                        filepath = os.path.join(root, filename)
                        translated_text += file_translator(filepath)

                output_file_path = os.path.join(output_directory, os.path.basename(file_path))
                with open(output_file_path, 'w') as output_file:
                    output_file.write(translated_text)

            else:
                return "Invalid File or Directory Path", 400
        else:
            return "File or Directory not found", 400

    else:
        # Checks to see if the text_response is a string
        translated_text = text_translator(input_text)
        return Response(translated_text, content_type='text/plain')
    
    return jsonify({'translated_text': translated_text})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=LIBRE_TRANSLATE_PORT, debug=False)
