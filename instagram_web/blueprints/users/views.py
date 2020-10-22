import os
from flask import  Flask, Blueprint, render_template, flash, redirect, url_for, request
from models.user import User
from models.image import Image
from flask_login import current_user, login_required
# upload image
from werkzeug.security import check_password_hash
from werkzeug import secure_filename
from helpers import upload_file_to_s3


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    newuser = User(username=username, email=email, password=password)

    if newuser.save():
        flash("New user successfully registered!")
        return redirect(url_for('users.new'))

    else:
        flash("User registration unsuccessful")
        return render_template('users/new.html', errors=newuser.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(User.username == username)
    # new
    images = Image.select().where(Image.user==user)
    return render_template("users/show.html", user=user, images=images)


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"

# edit profile here
@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id ==user.id:
            return render_template('users/edit.html', user=User.get_by_id(id))
        else:
            return "Breach"
    else:
        return 'No such user is found'


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_by_id(id)
    if current_user == user:
        new_user_name = request.form.get('new_user_name')
        new_email = request.form.get('new_email')
        new_password = request.form.get('new_password')
        user.username=new_user_name
        user.email=new_email
        user.password=new_password
        if user.save():
            flash('Successfully updated')
            return redirect(url_for('home'))
        else:
            flash(f"Unable to update, please try again")
            print(user.errors)
            return render_template('users/edit.html', user=user)

    else:
        flash('Unauthorised')
        return render_template('users/edit.html', user=user)


    # additional roles e.g. current_user.role = 'admin'

# upload image
@users_blueprint.route('/<id>/upload', methods=['GET'])
@login_required
def upload(id):
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id ==user.id:
            return render_template('users/upload.html', user=User.get_by_id(id))
        else:
            return "Breach"
    else:
        return 'No such user is found'

# why does it require a different root?
@users_blueprint.route("/<id>/upload_profile", methods=["POST"])
@login_required
def upload_profile(id):
    user = User.get_or_none(User.id == id)
    if user:
        if "user_file" not in request.files:
            return "No user_file key in request.files"

        file = request.files["user_file"]

        if file.filename == "":
            return "Please select a file"

        # here where it gets different
        if file:
            # included user.id this time, for no reason whatsoever
            # a: maybe, to be included as folder_name
            file_path = upload_file_to_s3(file, user.id)
            user.image_path = file_path
            if user.save():
                return redirect(url_for("users.show", username=user.username))
            else:
                return "Could not upload profile image, please go back and try again!"
        else:
            return redirect(url_for("users.upload", id=id))
    else:
        return "No such user!"
        
    #     if file and allowed_file(file.filename):
    #         file.filename = secure_filename(file.filename)
    #         output = upload_file_to_s3(file, app.config["S3_BUCKET"])
    #         return redirect(url_for('home'))

    #     else:
    #         return render_template("users/upload.html", user=user)
    # else:
    #     return 'No such user'

# EXTENSIONS FILE 

# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
