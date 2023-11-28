import peewee

from app.logic.gui import get_guis
from app.models.rpGUI import RpGUI

def test_get_gui():
    assert get_guis("Jetstream2") == "Exosphere, Horizon, CACAO"

def test_get_gui_not():
    assert get_guis("Jetstream2") != "Exposphere, Horizon"

def test_get_gui_type():
    assert isinstance(get_guis("Jetstream2"), peewee.ModelSelect)
    for gui in get_guis("JetStream2"):
        assert isinstance(gui, RpGUI)
"""
def test_get_gui_type_not():
    assert not isinstance(get_guis("Jetstream2"), str)
"""