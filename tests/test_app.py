from pathlib import Path
from tempfile import TemporaryDirectory  # noqa: F401

from src import app  # noqa: F401


def test_badwords(monkeypatch):
    app.profanity("fuck")
    assert False
