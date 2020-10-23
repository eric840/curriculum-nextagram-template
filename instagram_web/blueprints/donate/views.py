from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.image import Image
from helpers import get_client_token, create_donation

donate_blueprint = Blueprint('donate',
                            __name__,
                            template_folder='templates')

@donate_blueprint.route('/new', methods=['GET'])
def new(image_id):
    return render_template('donate/new.html', client_token=get_client_token() , image_id=image_id)

@donate_blueprint.route('/', methods=['POST'])
def create(image_id):
    image=Image.get_by_id(image_id)
    return redirect(url_for('users.show', id=image.user.id))




