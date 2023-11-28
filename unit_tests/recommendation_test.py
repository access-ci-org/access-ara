from app.logic.recommendation import calculate_points, classify_rp_storage

currentPoints = 0
suitability = 1

"""
This file contains different tests for the 'calculate_points' and 'classify_rp_storage' functions.
Ensure that the database was populated via 'source setup.sh test' before running tests.
In order to run tests, you must be in the access-ara directory; run tests by typing 'pytest' into the terminal.
"""

def test_calculate_points():
    assert calculate_points(currentPoints, suitability) == 1

def test_calculate_points_not():
    assert calculate_points(currentPoints, suitability) != 0

def test_calculate_points_type():
    assert type(calculate_points(currentPoints, suitability)) == int

def test_classify_rp_storage_long():
    classifiedRps = classify_rp_storage("long-term")
    assert classifiedRps['less-than-1'] == ['Bridges-2', 'Delta', 'Jetstream2', 'KyRIC', 'Open Science Grid', 'Open Storage Network']
    assert classifiedRps['1-10'] == ['ACES', 'DARWIN', 'Stampede-2']
    assert classifiedRps['more-than-10'] == ['Anvil', 'Expanse', 'FASTER', 'OOKAMI', 'Rockfish', 'RANCH']

def test_classify_rp_storage_scratch():
    classifiedRps = classify_rp_storage("scratch")
    assert classifiedRps['less-than-1'] == ['Bridges-2', 'Jetstream2', 'Stampede-2', 'RANCH', 'Open Science Grid', 'Open Storage Network']
    assert classifiedRps['1-10'] == ['ACES', 'DARWIN', 'Delta', 'FASTER', 'KyRIC', 'Rockfish']
    assert classifiedRps['more-than-10'] == ['Anvil', 'Expanse', 'OOKAMI']

def test_classify_rp_storage_type():
    assert isinstance(classify_rp_storage('long-term'), dict)
    assert isinstance(classify_rp_storage('scratch'), dict)
"""
def test_classify_rp_storage_type_not():
    assert not isinstance(classify_rp_storage('long-term'), str)
    assert not isinstance(classify_rp_storage('scratch'), str)
"""