from tempfile import TemporaryDirectory  # noqa: F401

from src import app, data  # noqa: F401
import pytest
import requests


def test_badwords(monkeypatch):

    assert app.profanity("fuck you")


@pytest.mark.vcr()
def test_translator():
    response = requests.post(app.LIBRE_TRANSLATE_PORT, data=data)
    assert b'Example domains' in response


# def test_file(monkeypatch):
# assert app.file_translator("input")