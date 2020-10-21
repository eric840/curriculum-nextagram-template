import os
from flask import  Flask, Blueprint, render_template, flash, redirect, url_for, request
from models.user import User
from flask_login import current_user

# not actually needed.
# app = Flask(__name__)

# app.secret_key = os.getenv('SECRET_KEY')

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
    # display username
    return username


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"

# edit profile here
@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    return render_template('users/edit.html', user=User.get_by_id(id))


@users_blueprint.route('/<id>', methods=['POST'])
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


