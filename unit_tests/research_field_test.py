import peewee

from app.logic.research import get_research_fields
from app.models.rpResearchField import RpResearchField

"""
This file contains different tests for the 'get_research_fields' function.
Ensure that the database was populated via 'source setup.sh test' before running tests.
In order to run tests, you must be in the access-ara directory; run tests by typing 'pytest' into the terminal.
"""

def test_get_research_fields():
    assert get_research_fields("KyRIC") == "Agriculture"

def test_get_research_fields_not():
    assert get_research_fields("KyRIC") != ""

def test_get_research_fields_type():
    assert isinstance(get_research_fields("KyRIC"), peewee.ModelSelect)
    for field in get_research_fields("Expanse"):
        assert isinstance(field, RpResearchField)