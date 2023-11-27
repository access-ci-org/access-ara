from . import *
from .rps import RPS

# Creates the model for RpInfo
class RpInfo(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    blurb = TextField()
    link = CharField(max_length=300)
    documentation = CharField(max_length=300)