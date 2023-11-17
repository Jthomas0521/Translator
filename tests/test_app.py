from tempfile import TemporaryDirectory  # noqa: F401

from src import app  # noqa: F401
import pytest
import requests
import os
from docx import Document


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


def test_docx(tmp_path, monkeypatch):
    target_language = "es"
    file_content = "The bird is blue."
    file_path = tmp_path / "sample.docx"

    doc = Document()
    doc.add_paragraph(file_content)
    doc.save(file_path)

    docx_text = app.text_translator(file_content, target_language)
    result = app.file_translator(str(file_path), target_language)
    assert result == docx_text


def test_pdf(tmp_path, monkeypatch):
    target_language = "fr"
    file_content = "the traffic today was horrible."
    file_path = tmp_path / "sample.pdf"

    with open(file_path, 'w') as file:
        file.write(file_content)

    test_text = app.text_translator(file_content, target_language)
    result = app.file_translator(str(file_path), target_language)
    assert result == test_text

# Example that works

# @pytest.mark.vcr()
# def test_iana():
#     response = requests.get('http://www.iana.org/domains/reserved')
#     assert response
