import os
import pathlib
import platform
import subprocess
from tkinter import ttk
from typing import Callable, TypeVar

import polars as pl

# Import constants


T = TypeVar("T")


def call_with_progress(
    func: Callable[..., T], progress_bar: ttk.Progressbar = None, *args, **kwargs
) -> T:
    result = func(*args, **kwargs)
    if progress_bar:
        progress_bar.step(1)
    return result


def letter_to_number(letter: str) -> int:
    """
    Converts a letter to its corresponding column number (1-indexed).
    :param letter: The letter to convert
    :return: The corresponding column number
    """
    return ord(letter.upper()) - ord("A")


def load_file(fp: pathlib.Path) -> pl.DataFrame:
    """
    Loads a file from the files directory and returns it as a polars DataFrame.
    :param fp: The file path
    :return: A polars DataFrame
    """
    print(f"Reading {fp.name}")
    if not fp.exists():
        raise FileNotFoundError(f"File {fp} does not exist.")
    return pl.read_excel(fp)


def open_file(file_path):
    output_file_path = pathlib.Path(file_path)
    if output_file_path.exists():
        if platform.system() == "Darwin":  # macOS
            subprocess.call(("open", output_file_path))
        elif platform.system() == "Windows":
            os.startfile(str(output_file_path))
        else:  # linux variants
            subprocess.call(("xdg-open", output_file_path))
