from . import *
from .gui import GUI
from .rps import RPS

class RpGUI(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    gui = ForeignKeyField(GUI, backref="rp_with_GUI")
    suitability = IntegerField(default=0)

