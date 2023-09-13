# from flask import Blueprint
# from flask import request, redirect, url_for

# routes = Blueprint('router', __name__)

# @routes.route('/r', methods=['GET'])
# def router():
#     to = request.args.get('to')

#     if to == "SignUp":
#         return redirect(url_for("SignUp"))
#     elif to == "LogIn":
#         return redirect(url_for("LogIn"))
    # elif to == "Home":
    #     return redirect(url_for("Home"))

from flask import Blueprint, redirect, url_for, abort,redirect, request 


routes = Blueprint('router', __name__)

# Created  a dictionary for mapping  'to' values to their corresponding endpoints.........
route_mapping = {
    'SignUp': 'SignUp',
    'LogIn': 'LogIn',
    'Home': 'Home',
}

@routes.route('/r', methods=['GET'])
def router():
    to = request.args.get('to')

    # Checking  if 'to' is in the dictionary, and if not,will  abort with a 404 error
    endpoint = route_mapping.get(to)
    if endpoint is None:
        abort(404)

    #  or else will redirect to the corresponding endpoint using url_for..
    return redirect(url_for(endpoint))
