from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re
# from flask_login import LoginManager
from flask_login import UserMixin
from playhouse.hybrid import hybrid_property

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password_hash = pw.CharField(unique=False)
    image_path= pw.CharField(null=True)
    password=None
    is_private=pw.BooleanField(null=True)

    @hybrid_property
    def profile_image_path(self):
        from app import app
        if self.image_path:
            return app.config.get("S3_LOCATION") + self.image_path
        else:
            pass

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_username and self.id != duplicate_username.id:
            self.errors.append(
                'Username is already taken. Please choose something else.')
        
        if duplicate_email and self.id != duplicate_email.id:
            self.errors.append(
                'Email is already taken. Please choose something else.')

        if self.password:
            if len(self.password) < 6:
                self.errors.append("Password must be at least 6 characters")

            if not re.search("[a-z]", self.password):
                self.errors.append("Password must include lowercase")

            if not re.search("[A-Z]", self.password):
                self.errors.append("Password must include uppercase")

            if not re.search("[\[\]\*\^\%@]", self.password):
                self.errors.append("Password must include special characters")

            if len(self.errors) == 0:
                print("No errors detected")
                self.password_hash = generate_password_hash(self.password)

        
        if not self.password_hash:
            self.errors.append("Password must be present")
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def follow(self,following):
        # cant call from the top, circular thingy
        from models.status import Status
        # get_by_id will trigger an error
        check_status=Status.get_or_none(follower=self.id, following=following)
        if check_status==None:
        # if self.follow_status(following) == None:
            new_status=Status(follower=self.id, following=following)
            if following.is_private == False:
                new_status.is_approved = True
            return new_status.save()
        else:
            # falsy will do 
            return  0

    def unfollow(self, following):
        from models.status import Status
        return Status.delete().where(Status.following==following, Status.follower==self.id).execute()

    def follow_status(self, following):
        from models.status import Status
        return Status.get_or_none(follower=self.id, following=following)

    @hybrid_property
    def followings(self):
        from models.status import Status
        followings_id=Status.select(Status.following).where(Status.follower==self.id, Status.is_approved==True)
        # followings=[]
        # for row in followings_row:
        #     followings.append(row.following)
        followings=User.select().where(User.id.in_(followings_id))
        # User.id.in_
        return followings

    @hybrid_property
    def followers(self):
        from models.status import Status
        followers_id=Status.select(Status.follower).where(Status.following==self.id, Status.is_approved==True)
        followers=User.select().where(User.id.in_(followers_id))
        return followers
    
    @hybrid_property
    def following_requests(self):
        from models.status import Status
        followings_id=Status.select(Status.following).where(Status.follower==self.id, Status.is_approved==False)
        followings=User.select().where(User.id.in_(followings_id))
        return followings

    @hybrid_property
    def follower_requests(self):
        from models.status import Status
        followers_id=Status.select(Status.follower).where(Status.following==self.id, Status.is_approved==False)
        followers=User.select().where(User.id.in_(followers_id))
        return followers

    def approve(self, follower):
        from models.status import Status
        change_status=Status.get_or_none(follower=follower, following=self.id)
        change_status.is_approved=True
        return change_status.save()


        

