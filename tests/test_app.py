from tempfile import TemporaryDirectory  # noqa: F401

from src import app  # noqa: F401
import pytest
import requests
import os
import json


def test_badwords(monkeypatch):

    assert app.profanity("fuck you")


@pytest.mark.vcr()
def test_translator(monkeypatch):
    LIBRE_TRANSLATE_URL = os.environ.get("LIBRE_TRANSLATE_URL")
    data = {'q': 'India gana la copa mundial después de 28 años', 'source': "es", 'target': "en"}
    response = requests.post(LIBRE_TRANSLATE_URL, data=data)

    # print(type(F_gen_response.text))
    json_response = json.loads(response.text)
    print(json_response)
    assert app.text_translator("India wins the world cup after 28 years")
    
@pytest.mark.vcr()
def test_translator_fake(monkeypatch):
    LIBRE_TRANSLATE_URL = os.environ.get("LIBRE_TRANSLATE_URL")
    data = {'q': 'India gana la copa mundial después de 28 años', 'source': "es", 'target': "en"}
    response = requests.post(LIBRE_TRANSLATE_URL, data=data)
    fake_text = "blahg balkeaeh oaedsfoih"

    # print(type(F_gen_response.text))
    json_response = json.loads(response.text)
    print(json_response)
    assert app.text_translator(fake_text == data)


def test_file():
    APP_DIRECTORY = os.environ.get("APP_DIRECTORY")
    test_path = os.path.join(APP_DIRECTORY, 'testfile.txt')
    assert app.file_translator(test_path)

# Example that works

# @pytest.mark.vcr()
# def test_iana():
#     response = requests.get('http://www.iana.org/domains/reserved')
#     assert response
