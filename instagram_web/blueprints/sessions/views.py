from flask import Flask, Blueprint, request, redirect, url_for, render_template, flash, session
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

sessions_blueprint = Blueprint('sessions',
                               __name__,
                               template_folder='templates')


@sessions_blueprint.route('/signin', methods=["GET"])
def show():
    return render_template('sessions/sign_in.html')


@sessions_blueprint.route('/', methods=["POST"])
def sign_in():
    username = request.form.get('username')
    password_to_check = request.form.get('password')

    user = User.get_or_none(User.username == username)

    if not user:
        flash(f"{username} is incorrect.")
        return render_template('sessions/sign_in.html')

    # the password is hashed.
    hashed_password = user.password

    if not check_password_hash(hashed_password, password_to_check):
        flash("Incorrect password! Please try again!")
        return render_template('sessions/sign_in.html')

    session['user_id'] = user.id
    flash(f"Welcome back {user.username}. You are logged in!")
    # don't have home here.
    return redirect(url_for('sessions.show'))

    # Use Flask-Login Package