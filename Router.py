from flask import Blueprint
from flask import request, redirect, url_for

routes = Blueprint('router', __name__)

@routes.route('/r', methods=['GET'])
def router():
    to = request.args.get('to')

    if to == "SignUp":
        return redirect(url_for("SignUp"))
    elif to == "LogIn":
        return redirect(url_for("LogIn"))
    elif to == "Home":
        return redirect(url_for("Home"))
