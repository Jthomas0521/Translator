from pathlib import Path
from tempfile import TemporaryDirectory  # noqa: F401

from src import app  # noqa: F401


def test_badwords(monkeypatch):

    assert app.profanity("fuck you")


def test_translator(monkeypatch):

    assert app.text_translator("hola")


def file_translator(monkeypatch):

    assert app.file_translator()