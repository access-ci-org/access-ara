from ..models.rps import RPS
from ..models.rpGUI import RpGUI

def get_guis(rpName):
    rp = RPS.select().where(RPS.name==rpName)
    guis = RpGUI.select().where(RpGUI.rp == rp).order_by(RpGUI.rp.name)
    return(guis)