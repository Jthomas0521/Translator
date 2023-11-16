import os
from flask import Flask, request, render_template, Response
import requests
import logging
from dotenv import load_dotenv
import json
from docx import Document
import PyPDF2

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
def profanity(text: str) -> bool:
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


# Translated DOCX file
def docx_translator(file_path: str, target_language: str) -> str:
    docx_file = Document(file_path)
    docx_text = []

    for paragraph in docx_file.paragraphs:
        docx_text.append(paragraph.text)
    input_text = ''.join(docx_text)
    return text_translator(input_text, target_language)


# Translated PDF file
def pdf_translator(file_path: str, target_language: str) -> str:
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        input_text = ''

        for page_num in range(pdf_reader):
            pdf_page = pdf_reader.getPage(page_num)
            input_text += pdf_page.extractText()
        return text_translator(input_text, target_language)


# Translated Text
def text_translator(text: str, target_language: str) -> Response:
    LIBRE_TRANSLATE_URL = os.environ.get("LIBRE_TRANSLATE_URL")
    data = {'q': text, 'source': "auto", 'target': target_language}
    gen_response = requests.post(LIBRE_TRANSLATE_URL, data=data)
    json_response = json.loads(gen_response.text)

    logger.info(f"Translation Status Code: {gen_response.status_code}")
    logger.info(f"Translation Response Text: {gen_response.text}")

    if gen_response.status_code == 200:
        return json_response["translatedText"]
    logger.info(f"Translation error: {json_response.status_code}")


# Translated text file
def file_translator(file_path: str, target_language: str) -> str:
    if file_path.endswith('.docx'):
        input_text = docx_translator(file_path, target_language)
    elif file_path.endswith('.docx'):
        input_text = pdf_translator(file_path, target_language)
    else:
        with open(file_path, 'r') as file:
            input_text = file.read()
    file_response = text_translator(input_text, target_language)

    # Checks to see if file_response produces an instance in Response
    if isinstance(file_response, Response):
        return file_response.text
    else:
        logger.info("Not an instance of Response")
    return file_response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    input_text = request.form.get('input_text')
    file_path = request.form.get('file_path')
    target_language = request.form.get('target_language')

    translated_text = None

    if profanity(input_text):
        return "Profanity Detected. Please Remove."

    if file_path:
        file_path = os.path.join(APP_DIRECTORY, file_path)

        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                translated_text = file_translator(file_path, target_language)
            elif os.path.isdir(file_path):
                translated_text = ""

                for root, files in os.walk(file_path):
                    for filename in files:
                        filepath = os.path.join(root, filename)
                        translated_text += file_translator(filepath, target_language)

                output_file_path = os.path.join(output_directory, os.path.basename(file_path))
                with open(output_file_path, 'w') as output_file:
                    output_file.write(translated_text)

            else:
                return "Invalid File or Directory Path", 400
        else:
            return "File or Directory not found", 400

    else:
        # Checks to see if the text_response is a string
        translated_text = text_translator(input_text, target_language)

    return render_template('index.html', translated_text=translated_text)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=LIBRE_TRANSLATE_PORT, debug=False)
