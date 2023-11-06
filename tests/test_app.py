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
    data = {'q': "India wins the world cup after 28 years", 'source': "en", 'target': "hi", 'format': "text"}
    F_gen_response = requests.post(LIBRE_TRANSLATE_URL, data=data)

    if F_gen_response.status_code == 200:
        # print(type(F_gen_response.text))
        json_response = json.loads(F_gen_response.text)
        assert json_response['translatedText']


def test_file():
    APP_DIRECTORY = os.environ.get("APP_DIRECTORY")
    test_path = os.path.join(APP_DIRECTORY, 'testfile.txt')
    assert app.file_translator(test_path)

# Example that works

# @pytest.mark.vcr()
# def test_iana():
#     response = requests.get('http://www.iana.org/domains/reserved')
#     assert response
