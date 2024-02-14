from . import *

class RPS(BaseModel):
    id = PrimaryKeyField()
    name = CharField(unique=True, constraints=[SQL('COLLATE NOCASE')])
    scratch_tb = FloatField()
    longterm_tb = FloatField()
    gpu = IntegerField(default=0)
    graphical = IntegerField(default=0)
    virtual_machine = IntegerField(default=0)
