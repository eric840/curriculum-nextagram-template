from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donate.views import donate_blueprint

from flask_assets import Environment, Bundle
from .util.assets import bundles
# flask-login
from flask_login import LoginManager
from models.user import User
# oauth
from helpers import oauth

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donate_blueprint, url_prefix="/images/<image_id>/donate")

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)

# oauth
oauth.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)
# endof flask-login

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def home():
    return render_template('home.html')
