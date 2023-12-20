#import pytest
import peewee

from app.logic.softwares import get_softwares
from app.models.rpSoftware import RpSoftware

"""
This file contains different tests for the 'get_softwares' function.
Ensure that the database was populated via 'source setup.sh test' before running tests.
In order to run tests, you must be in the access-ara directory; run tests by typing 'pytest' into the terminal.
"""

def test_get_softwares():
    assert get_softwares("ACES") == "Pytorch, Tensorflow"

def test_get_softwares_not():
    assert get_softwares("ACES") != ""

def test_get_softwares_type():
    assert isinstance(get_softwares("ACES"), peewee.ModelSelect)
    for software in get_softwares("ACES"):
        assert isinstance(software, RpSoftware)