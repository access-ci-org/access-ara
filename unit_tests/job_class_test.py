import peewee

from app.logic.jobClass import get_job_classes
from app.models.rpJobClass import RpJobClass

"""
This file contains different tests for the 'get_job_classes' function.
Ensure that the database was populated via 'source setup.sh test' before running tests.
In order to run tests, you must be in the access-ara directory; run tests by typing 'pytest' into the terminal.
"""

def test_get_job_classes():
    assert get_job_classes("Bridges-2") == "Data Analytics, Machine Learning"

def test_get_job_classes_not():
    assert get_job_classes("Bridges-2") != ""

def test_get_job_classes_type():
    assert isinstance(get_job_classes("Bridges-2"), peewee.ModelSelect)
    for job in get_job_classes("Bridges-2"):
        assert isinstance(job, RpJobClass)
"""
def test_get_job_classes_type_not():
    assert not isinstance(get_job_classes("Bridges-2"), str)
"""