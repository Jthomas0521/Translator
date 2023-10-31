from tempfile import TemporaryDirectory  # noqa: F401

from src import app  # noqa: F401
import pytest
import requests
import os


def test_badwords(monkeypatch):

    assert app.profanity("fuck you")


#@pytest.mark.vcr()
def test_translator():
    LIBRE_TRANSLATE_URL = os.environ.get("LIBRE_TRANSLATE_URL")
    data = {'input_text'}
    gen_response = requests.post(LIBRE_TRANSLATE_URL, data=data)
    assert b'Example domains' in gen_response


# def test_file(monkeypatch):
# assert app.file_translator("input")
