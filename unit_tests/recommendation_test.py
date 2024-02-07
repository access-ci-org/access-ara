import pytest
from app.logic.recommendation import calculate_points, classify_rp_storage, calculate_score_rf, calculate_score_software, get_recommendations


"""
This file contains different tests for the functions in app/logic/recommendation.py.
Ensure that the database was populated via 'source setup.sh test' before running tests.
In order to run tests, you must be in the access-ara directory; run tests by typing 'pytest' into the terminal.
"""

#Simple parameters for testing calculate_points() function
currentPoints = 0
suitability = 1

def test_calculate_points():
    assert calculate_points(currentPoints, suitability) == 1

def test_calculate_points_not():
    assert calculate_points(currentPoints, suitability) != 0

def test_calculate_points_type():
    assert type(calculate_points(currentPoints, suitability)) == int

#Check to see that test data is segmented correctly for long-term storage
def test_classify_rp_storage_long():
    classifiedRps = classify_rp_storage("long-term")
    assert classifiedRps['less-than-1'] == ['Bridges-2', 'Delta', 'Jetstream2', 'KyRIC', 'Open Science Grid', 'Open Storage Network']
    assert classifiedRps['1-10'] == ['ACES', 'DARWIN', 'Stampede-2']
    assert classifiedRps['more-than-10'] == ['Anvil', 'Expanse', 'FASTER', 'OOKAMI', 'Rockfish', 'RANCH']

#Check to see that test data is segmeneted correctly for short-term (scratch) storage
def test_classify_rp_storage_scratch():
    classifiedRps = classify_rp_storage("scratch")
    assert classifiedRps['less-than-1'] == ['Bridges-2', 'Jetstream2', 'Stampede-2', 'RANCH', 'Open Science Grid', 'Open Storage Network']
    assert classifiedRps['1-10'] == ['ACES', 'DARWIN', 'Delta', 'FASTER', 'KyRIC', 'Rockfish']
    assert classifiedRps['more-than-10'] == ['Anvil', 'Expanse', 'OOKAMI']

def test_classify_rp_storage_type():
    assert isinstance(classify_rp_storage('long-term'), dict)
    assert isinstance(classify_rp_storage('scratch'), dict)

"""
In the following 'calculate score' tests, the scoreboard keeps points added from prior 'calculate score' tests.
Running them in a different order would yield slightly different results, but the final scoreboard will be the same.
"""

#Simple parameters for testing
researchFieldList = ['Civil Engineering', 'Computer Science']
scoreboard = {}

def test_calculate_score_rf():
    assert calculate_score_rf(researchFieldList, scoreboard) == {'Jetstream2': {'score': 1, 'reasons': ['Civil Engineering']},
                                                                 'Bridges-2': {'score': 2, 'reasons': ['Civil Engineering', 'Computer Science']},
                                                                 'Stampede-2': {'score': 1, 'reasons': ['Computer Science']},
                                                                 'Expanse': {'score': 1, 'reasons': ['Computer Science']}}

softwareList = ['GCC', 'TensorFlow']

def test_calculate_score_software():
    assert calculate_score_software(softwareList, scoreboard) == {'Jetstream2': {'score': 1, 'reasons': ['Civil Engineering']},
                                                                'Bridges-2': {'score': 22, 'reasons': ['Civil Engineering', 'Computer Science', 'gcc', 'tensorflow']},
                                                                'Stampede-2': {'score': 11, 'reasons': ['Computer Science', 'gcc']},
                                                                'Expanse': {'score': 11, 'reasons': ['Computer Science', 'gcc']},
                                                                'Delta': {'score': 10, 'reasons': ['gcc']},
                                                                'DARWIN': {'score': 10, 'reasons': ['tensorflow']},
                                                                'ACES': {'score': 20, 'reasons': ['gcc', 'tensorflow']},
                                                                'FASTER': {'score': 10, 'reasons': ['gcc']},
                                                                'OOKAMI': {'score': 10, 'reasons': ['gcc']},
                                                                'Rockfish': {'score': 20, 'reasons': ['gcc', 'tensorflow']}}

formData = {'hpc-use': '1', 'access-familiarity': '1', 'used-hpc': ['Bridges-2', 'Delta', 'FASTER', 'KyRIC'],
            'hpc-experience': '4+ years', 'gui-needed': '1', 'used-gui': ['Open OnDemand'],
            'storage': '1', 'num-files': '', 'long-term-storage': 'less-than-1', 'temp-storage': '1-10',
            'memory': 'more-than-512', 'software': 'tensorflow,gcc', 'graphics': '1', 'gpu': '1',
            'job-run': '0', 'vm': '0', 'research-field': 'Civil Engineering,Computer Science', 'add-field-tags': '',
            'add-software-tags': '', 'job-class': 'Machine Learning,Deep Learning', 'add-job-tags': ''}

badFormData = {'Hello': '123'}

def test_get_recommendations():
    assert get_recommendations(formData) == {'Bridges-2': {'score': 29, 'reasons': ['User Experience', 'Open OnDemand', 'Civil Engineering', 'Computer Science', 'Long Term Storage', 'gcc', 'tensorflow', 'Graphics', 'GPU']},
                                             'Delta': {'score': 17, 'reasons': ['User Experience', 'Long Term Storage', 'Temporary Storage', '2000 GB Memory', 'gcc', 'Graphics', 'GPU']},
                                             'FASTER': {'score': 17, 'reasons': ['User Experience', 'Open OnDemand', 'Temporary Storage', 'gcc', 'Graphics', 'GPU']},
                                             'KyRIC': {'score': 6, 'reasons': ['User Experience', 'Long Term Storage', 'Temporary Storage', '3000 GB Memory', 'Graphics']},
                                             'Expanse': {'score': 16, 'reasons': ['Open OnDemand', 'Computer Science', '2000 GB Memory', 'gcc', 'Graphics', 'GPU']},
                                             'Anvil': {'score': 3, 'reasons': ['Open OnDemand', '1000 GB Memory', 'GPU']},
                                             'ACES': {'score': 25, 'reasons': ['Open OnDemand', 'Temporary Storage', 'gcc', 'tensorflow', 'Graphics', 'GPU']},
                                             'Jetstream2': {'score': 4, 'reasons': ['Civil Engineering', 'Long Term Storage', '1024 GB Memory', 'GPU']},
                                             'Stampede-2': {'score': 13, 'reasons': ['Computer Science', 'gcc', 'Graphics']},
                                             'Open Science Grid': {'score': 2, 'reasons': ['Long Term Storage', 'GPU']},
                                             'Open Storage Network': {'score': 1, 'reasons': ['Long Term Storage']},
                                             'DARWIN': {'score': 16, 'reasons': ['Scratch Storage', '1024 GB Memory', '2048 GB Memory', 'tensorflow', 'Graphics', 'GPU']},
                                             'Rockfish': {'score': 23, 'reasons': ['Scratch Storage', '1500 GB Memory', 'gcc', 'tensorflow', 'GPU']},
                                             'OOKAMI': {'score': 11, 'reasons': ['gcc', 'GPU']}}


    with pytest.raises(AttributeError):
        get_recommendations(badFormData)
