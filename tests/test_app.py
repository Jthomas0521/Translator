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
    assert app.text_translator("India wins the world cup after 28 years")

    """
    LIBRE_TRANSLATE_URL = os.environ.get("LIBRE_TRANSLATE_URL")
    data = {'q': 'India gana la copa mundial después de 28 años', 'source': "es", 'target': "en"}
    response = requests.post(LIBRE_TRANSLATE_URL, data=data)

    # print(type(F_gen_response.text))
    json_response = json.loads(response.text)
    expected_text = "India wins the world cup after 28 years"
    assert json_response["translatedText"] == expected_text
    """


@pytest.mark.vcr()
def test_translator_fake(monkeypatch):
    LIBRE_TRANSLATE_URL = os.environ.get("LIBRE_TRANSLATE_URL")
    fake_text = "Go Jets Go."

    data = {'q': fake_text, 'source': "auto", 'target': "fr"}
    # data = {'q': 'India gana la copa mundial después de 28 años', 'source': "es", 'target': "fr"}
    response = requests.post(LIBRE_TRANSLATE_URL, data=data)

    json_response = response.json()
    translated_text = json_response["translatedText"]
    # assert translated_text != fake_text
    assert app.text_translator(translated_text)


def test_file():
    APP_DIRECTORY = os.environ.get("APP_DIRECTORY")
    test_path = os.path.join(APP_DIRECTORY, 'testfile.txt')

    # response = app.file_translator(test_path)
    # assert isinstance(response, str)
    assert app.file_translator(test_path)


# Example that works

# @pytest.mark.vcr()
# def test_iana():
#     response = requests.get('http://www.iana.org/domains/reserved')
#     assert response
