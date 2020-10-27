import peewee as pw
from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property

class Status(BaseModel):
    # do you need backref here?
    following = pw.ForeignKeyField(User, on_delete="CASCADE")
    follower = pw.ForeignKeyField(User, on_delete="CASCADE")
    is_approved = pw.BooleanField(null=False, default=False)