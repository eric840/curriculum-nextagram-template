import peewee as pw
from models.base_model import BaseModel
from models.user import User
from playhouse.hybrid import hybrid_property


class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref="images", on_delete="CASCADE")
    image_url = pw.TextField(null=False)

    @hybrid_property
    def full_image_url(self):
        from app import app
        if self.image_url:
            return app.config.get("S3_LOCATION") + self.image_url
        else:
            pass

    @hybrid_property
    def donations_sum(self):
        result = 0
        for d in self.donations:
            result += d.amount
        return result