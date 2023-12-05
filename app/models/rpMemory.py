from . import *
from .rps import RPS

# Creates the model for RpMemory
class RpMemory(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    node_type = CharField(max_length=40)
    per_node_memory_gb = IntegerField(default=0)
