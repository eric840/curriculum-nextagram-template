from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.image import Image
from models.donate import Donate
from helpers import get_client_token, create_donation
from braintree.successful_result import SuccessfulResult
from flask_login import current_user, login_required

donate_blueprint = Blueprint('donate',
                            __name__,
                            template_folder='templates')

@donate_blueprint.route('/new', methods=['GET'])
def new(image_id):
    return render_template('donate/new.html', client_token=get_client_token() , image_id=image_id)

@donate_blueprint.route('/', methods=['POST'])
def create(image_id):
    data=request.form
    image=Image.get_by_id(image_id)
    result = create_donation(data.get("amount"),data.get("payment_method_nonce"))
    if type(result) == SuccessfulResult:
        new_donation = Donate(amount = data.get("amount"), image=image, user= current_user.id )
        if new_donation.save():
            return redirect(url_for("users.show",username = image.user.username))
        else:
            return "Could not save transaction"
    else:
        return "Could not create braintree transaction"




