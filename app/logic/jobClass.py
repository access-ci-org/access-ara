from ..models.rps import RPS
from ..models.rpJobClass import RpJobClass

def get_job_classes(rpName):
    """
    get the job classes associated with the rpName
    returns a peewee ModelSelect object
    """
    rp = RPS.select().where(RPS.name==rpName)
    jobClasses = RpJobClass.select().where(RpJobClass.rp == rp).order_by(RpJobClass.rp.name)
    return jobClasses
