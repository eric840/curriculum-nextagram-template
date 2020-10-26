import peewee as pw
from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property

class Status(BaseModel):
    following = pw.ForeignKeyField(User, backref="following", on_delete="CASCADE")
    follower = pw.ForeignKeyField(User, backref="follower", on_delete="CASCADE")
    authorized = pw.BooleanField(null=False)