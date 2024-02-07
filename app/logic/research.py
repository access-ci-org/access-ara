from ..models.rpResearchField import RpResearchField
from ..models.rps import RPS

def get_research_fields(rpName):
    """
    get the research fields associated with the rpName
    returns a peewee ModelSelect object
    """
    rp = RPS.select().where(RPS.name==rpName)
    researchFields = RpResearchField.select().where(RpResearchField.rp == rp).order_by(RpResearchField.rp.name)
    return(researchFields)