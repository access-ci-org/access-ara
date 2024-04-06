from . import *

class Software(BaseModel):
    id = PrimaryKeyField()
    software_name = CharField(unique=True, constraints=[SQL('COLLATE NOCASE')])
    version = CharField(default='')