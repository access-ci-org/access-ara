import peewee

from app.logic.gui import get_guis
from app.models.rpGUI import RpGUI

"""
This file contains different tests for the 'get_guis' function.
Ensure that the database was populated via 'source setup.sh test' before running tests.
In order to run tests, you must be in the access-ara directory; run tests by typing 'pytest' into the terminal.
"""

def test_get_gui():
    assert get_guis("Jetstream2") == "Exosphere, Horizon, CACAO"

def test_get_gui_not():
    assert get_guis("Jetstream2") != "Exposphere, Horizon"

def test_get_gui_type():
    assert isinstance(get_guis("Jetstream2"), peewee.ModelSelect)
    for gui in get_guis("JetStream2"):
        assert isinstance(gui, RpGUI)
