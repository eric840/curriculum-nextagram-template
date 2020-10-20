from models.base_model import BaseModel
import peewee as pw
from werkzeug.security import generate_password_hash
import re
from flask_login import LoginManager

class User(BaseModel):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password_hash = pw.CharField(unique=False)
    password=None

    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        if duplicate_username:
            # i dont remember where/when this shows
            self.errors.append(
                'Username is already taken. Please choose something else.')
        
        if duplicate_email:
            self.errors.append(
                'Username is already taken. Please choose something else.')

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