import peewee as pw
from models.base_model import BaseModel
from models.user import User
from models.image import Image
from playhouse.hybrid import hybrid_property


class Donate(BaseModel):
    # what is backref, and on_delete?
    image= pw.ForeignKeyField(Image, backref="donations", on_delete="CASCADE")
    user= pw.ForeignKeyField(User, backref="donations", on_delete="CASCADE")
    amount= pw.DecimalField(null=False)
