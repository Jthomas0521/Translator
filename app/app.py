import os
from flask import Flask, request, render_template, Response
# from libretranslate import LibreTranslate
import requests

app = Flask(__name__)

# libretranslate = LibreTranslate(target_language="en")

# Requests the current directory
app_directory = os.path.dirname(__file__)
profanity_words = os.path.join(app_directory, 'badwords.txt')


# Profanity Words Checker
def profanity(text):
    with open(profanity_words, 'r') as file:
        badwords = set(word.strip() for word in file)

        # Splits the words
        words = text.lower().split()

        # Detects if any words  from the text are identified in the badwords.txt file
        for word in words:
            if word in badwords:
                return True
        return False


# Directory paths for input and output volumes
input_directory = os.path.join(app_directory, 'input')
output_directory = os.path.join(app_directory, 'output')

# Input and Output Directories
os.makedirs(input_directory, exist_ok=True)
os.makedirs(output_directory, exist_ok=True)


# Translated Text
def translated_text(text):
    libretranslate_page = 'http://libretranslate:8000/translate'
    data = {'input_text': text}
    response = requests.post(libretranslate_page, data=data)
    return response


# Translated text pille
def translated_file(file_path):
    with open(file_path, 'r') as file:
        input_text = file.read()
        response = translated_text(input_text)
        return response.text


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
        file_path = os.path.join(app_directory, file_path)

        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                translated_text = translated_file(file_path)
            elif os.path.isdir(file_path):
                translated_text = ""

                for root, dirs, files in os.walk(file_path):
                    for filename in files:
                        filepath = os.path.join(root, filename)
                        translated_text += translated_file(filepath)

                output_file_path = os.path.join(output_directory, os.path.basename(file_path))
                with open(output_file_path, 'w') as output_file:
                    output_file.write(translated_text)

            else:
                return "Invalid File or Directory Path", 400
        else:
            return "File or Directory not found", 400

    else:
        response = translated_text(input_text)
        if response.status_code != 200:
            return f"Translation error: {response.status_code}", 500
        translated_text = response.text

    return Response(translated_text, content_type='text/plain')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
