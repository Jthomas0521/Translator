import os
import pathlib


def analyze_data(file: str):
    try:
        with open(file) as fp:
            data = fp.read()
            ...
    except FileNotFoundError:
        print(f"Does not exist, exiting: {file}")
    except IsADirectoryError:
        ...