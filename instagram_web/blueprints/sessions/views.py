from flask import Flask, Blueprint, request, redirect, url_for, render_template, flash, session
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
# flask-login
from flask_login import login_user, logout_user, login_required, current_user

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route('/signin', methods=["GET"])
def show():
    return render_template('sessions/signin.html')


@sessions_blueprint.route('/', methods=["POST"])
def sign_in():
    username = request.form.get('username')
    password_to_check = request.form.get('password')

    user = User.get_or_none(User.username == username)

    if not user:
        flash(f"{username} is incorrect.")
        return render_template('sessions/signin.html')

    # the password is hashed.
    hashed_password = user.password_hash

    if not check_password_hash(hashed_password, password_to_check):
        flash("Incorrect password! Please try again!")
        return render_template('sessions/signin.html')

    # session login
    # session['user_id'] = user.id

    # flask-login
    login_user(user)

    flash(f"Welcome back {user.username}. You are logged in!")
    # don't have home here.
    return redirect(url_for('sessions.show'))

# flask-login
@sessions_blueprint.route("/settings")
@login_required
def settings():
    pass

@sessions_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('sessions.show'))