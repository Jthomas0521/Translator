from tempfile import TemporaryDirectory  # noqa: F401

from src import app  # noqa: F401
import pytest
import requests
import os
# import json


def test_badwords(monkeypatch):
    assert app.profanity("fuck you")


@pytest.mark.vcr()
def test_translator(monkeypatch):
    target_language = "es"
    assert app.text_translator("India wins the world cup after 28 years", target_language)


@pytest.mark.vcr(record_mode='new_episodes')
def test_translator_fake(monkeypatch):
    LIBRE_TRANSLATE_URL = os.environ.get("LIBRE_TRANSLATE_URL")
    fake_text = "Go Jets Go."
    target_language = "fr"

    data = {'q': fake_text, 'source': "auto", 'target': target_language}
    response = requests.post(LIBRE_TRANSLATE_URL, data=data)

    json_response = response.json()
    translated_text = json_response["translatedText"]

    result = app.text_translator(translated_text, target_language)
    assert result


def test_file():
    APP_DIRECTORY = os.environ.get("APP_DIRECTORY")
    test_path = os.path.join(APP_DIRECTORY, 'testfile.txt')
    target_language = "ar"

    assert app.file_translator(test_path, target_language)


def test_docx(tmp_path, mocker, monkeypatch):
    target_language = "fr"
    translated_text = "Translated Docx Text"
    file_content = "Docx Content"
    file_path = tmp_path / "sample.docx"
    
    with open(file_path, 'w') as file:
        file.write(file_content)
        
    mocker.patch('src.app.text_translator', return_value=translated_text)
    result = app.file_translator(str(file_path), target_language)
    assert result == translated_text
    

def test_pdf(tmp_path, mocker, monkeypatch):
    target_language = "fr"
    translated_text = "Translated PDF Text"
    file_content = "PDF COntent"
    file_path = tmp_path / "sample.pdf"
    
    with open(file_path, 'w') as file:
        file.write(file_content)
        
    mocker.patch('src.app.text_translator', return_value=translated_text)
    result = app.file_translator(str(file_path), target_language)
    assert result == translated_text

# Example that works

# @pytest.mark.vcr()
# def test_iana():
#     response = requests.get('http://www.iana.org/domains/reserved')
#     assert response
