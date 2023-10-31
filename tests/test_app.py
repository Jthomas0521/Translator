from tempfile import TemporaryDirectory  # noqa: F401

from src import app  # noqa: F401
import pytest
import requests
import os


def test_badwords(monkeypatch):

    assert app.profanity("fuck you")


@pytest.mark.vcr()
def test_translator():
    LIBRE_TRANSLATE_URL = os.environ.get("LIBRE_TRANSLATE_URL")
    data = {'q': "India wins the world cup after 28 years", 'source': "en", 'target': "hi", 'format': "text"}
    gen_response = requests.post(LIBRE_TRANSLATE_URL, data=data)
    # assert {"भारत ने 28 साल बाद विश्व कप जीता"} in gen_response
    # assert True
    # assert app.text_translator(gen_response)
    assert gen_response


# def test_file(monkeypatch):
# assert app.file_translator("input")

# Example that works

# @pytest.mark.vcr()
# def test_iana():
#     response = requests.get('http://www.iana.org/domains/reserved')
#     assert response
