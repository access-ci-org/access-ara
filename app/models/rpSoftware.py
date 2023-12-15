from . import *
from .software import Software
from .rps import RPS

class RpSoftware(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    software = ForeignKeyField(Software, backref="rp_with_Software")